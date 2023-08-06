# -*- coding: utf-8 -*-
"""
Module worker.py:
--------------------------
    The long running worker class implementation.
"""
import sys
import os
import signal
import traceback
from enum import Enum
from . import utils
from . import exceptions
from .processor import Register
from .message import Message, MessageStatus
from datetime import datetime
from .queue import Queue
import blinker


class WorkerStatus(Enum):
    """
    Enum of worker possible status.
    """
    STARTING = 'starting'
    STARTED = 'started'
    SUSPENDED = 'suspended'
    BUSY = 'busy'
    IDLE = 'idle'


# processor registry instance
registry = Register()


class Worker(object):
    """
    A Simple Queue worker class.
    """
    def __init__(self, queue, logger, sqs, dl_queue=None, max_receive_count=10, message_wait_time=20, visibility_timeout=60):  # noqa
        """
        Worker initialization function.
        :param queue: the queue name.
        :param logger: the logger to be used by the worker.
        :param sqs: A boto3.Resource object for the AWS.SQS.
        :param dl_queue: The name of the deadLetter Queue.
        :param max_receive_count: The maximum number of re-drives before send a message to the dead letter. 
        :param message_wait_time: Polling wait time in seconds.
        :param visibility_timeout: SQS Visibility Timeout configuration.
        See https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html
        for mor information on that.
        """
        if sqs is None:
            raise ValueError("Sqs resource can not be None.")
        self.sqs = sqs
        self.client = sqs.meta.client
        self.max_receive_count = max_receive_count
        self.message_wait_time = message_wait_time
        self.visibility_timeout = visibility_timeout
        self.queue_name = queue
        self.dl_queue_name = dl_queue
        # instantiate the queue object.
        self.queue = Queue(
            queue_name=self.queue_name,
            sqs=self.sqs,
            dl_queue=self.dl_queue_name,
            max_receive_count=self.max_receive_count,
            message_wait_time=self.message_wait_time,
            visibility_timeout=self.visibility_timeout
        )

        # other information that are worth to keep
        self._state = WorkerStatus.STARTING
        self._stop_requested = False
        self.log = logger
        self.successful_job_count = 0
        self.failed_job_count = 0
        self.total_working_time = 0
        self.birth_date = None

        # worker events
        self.on_job_failure = blinker.signal("on-job-failure")
        self.after_job_done = blinker.signal("after-job-done")
        self.before_receive_msg = blinker.signal("before-receive-msg")

    def _install_signal_handlers(self):
        """Installs signal handlers for handling SIGINT and SIGTERM
        gracefully.
        """
        signal.signal(signal.SIGINT, self.request_stop)
        signal.signal(signal.SIGTERM, self.request_stop)

    def request_force_stop(self, signum, frame):
        """Terminates the application (cold shutdown).
        """
        self.log.warning('Cold shut down.')
        raise SystemExit()

    def request_stop(self, signum, frame):
        """Stops the current worker loop but waits for child processes to
        end gracefully (warm shutdown).
        """
        self.log.debug('Got signal %s', utils.signal_name(signum))

        signal.signal(signal.SIGINT, self.request_force_stop)
        signal.signal(signal.SIGTERM, self.request_force_stop)

        self.handle_warm_shutdown_request()

        # If shutdown is requested in the middle of a job, wait until
        # finish before shutting down and save the request in redis
        if self.state == WorkerStatus.BUSY:
            self.log.debug('Stopping after current job is done. '
                           'Press Ctrl+C again for a cold shutdown.')
        else:
            raise exceptions.StopRequested()

    def handle_warm_shutdown_request(self):
        self.log.warning('Warm shut down requested')
        self._stop_requested = True

    def work(self, burst=False):
        """Starts the work loop.

        Pops and process messages from the current queue.  When the
        queue is empty, block and wait for new message to arrive, 
        unless `burst` mode is enabled.

        The return value indicates whether any jobs were processed.
        """
        self._install_signal_handlers()
        self.log.info("Simple-Queue Worker Started.")
        self.state = WorkerStatus.STARTED
        self.log.info('*** Listening on {}...'.format(self.queue_name))
        did_perform_work = True
        try:
            while not self._stop_requested:
                try:
                    # before receive message event hook
                    self.before_receive_msg.send(self)
                    # receives queue messages
                    for msg in self.queue.receive_messages():
                        if self._stop_requested:
                            self.log.info('Stopping on request.')
                            break
                        if msg is None:
                            if burst:
                                self.log.info("Simple-Worker {0!r} done, quitting.".format(os.getpid()))
                                self._stop_requested = True
                                break
                        else:
                            self.execute(msg)
                except exceptions.StopRequested:
                    self._stop_requested = True
                    did_perform_work = False
        finally:
            self.log.info(
                "Stopping the worker..."
            )
        return did_perform_work

    def dispatch_message(self, message: Message):  # noqa
        """Invokes the processor function with the message."""
        # check if title is registered
        if message.title not in registry:
            raise ValueError(
                "Could not find a Handler for the message titled as '{0}' in the registry object."
                "Please, Check if the handler is implemented correctly.\n\n"
                "Message.id: {1}.\n".format(
                    message.title,
                    message.id
                )
            )

        # gets the message handler
        handler = registry[message.title]
        # sanity check in action function
        message._result = handler.dispatch_message(message)

        return message._result

    def handle_job_failure(self, message:Message):
        """Handles the failure or an executing job by logging the error.
        """
        try:
            exc_info = sys.exc_info()
            exc_string = utils.get_safe_exception_string(
                traceback.format_exception_only(*exc_info[:2]) + traceback.format_exception(*exc_info)
            )
            # on job fail event hook
            self.on_job_failure.send(self)
            # logging error
            self.log.error(
                "Error from message: \n"
                "Message.title: {} \n"
                "Message.id: {} \n"
                "Message.body: {} \n"
                "Message.kwargs: {} \n"
                "Message.origin: {} \n"
                "ExceptionString: \n\t{}".format(
                    message.title,
                    message.id,
                    message.body.to_dict(),
                    message.kwargs,
                    message.origin,
                    exc_string
                ),
                exc_info=True
            )
        except Exception:
            # Ensure that custom exception handlers are called
            # even if Redis is down
            pass

    def execute(self, msg: Message):
        """Performs the actual work of a job.  
        It Parses the message received from the queue and dispatches it to the handler.
        """
        try:
            self.state = WorkerStatus.BUSY
            ret = self._execute(msg)
            # if success
            if ret:
                # then send ok confirmation to the queue
                msg.ok()
                # after job done event hook
                self.after_job_done.send(self)

        except Exception as e:
            self.log.error(
                "Error while processing the message.\n"
                "Message.title: {} \n"
                "Message.id: {} \n"
                "Message.body: {} \n"
                "Message.kwargs: {} \n"
                "Message.origin: {} \n\n"
                "Exception Message: \n"
                "\t {}".format(
                    msg.title,
                    msg.id,
                    msg.body.to_dict(),
                    msg.kwargs,
                    msg.origin,
                    str(e)
                ),
                exc_info=True
            )
        finally:
            self.state = WorkerStatus.IDLE

    def _execute(self, message:Message):
        """Performs the actual work of a job.  
        It Parses the message received from the queue and dispatches it to the handler.
        """
        try:
            message.started_at = datetime.utcnow()
            message.status = MessageStatus.Processing
            self.dispatch_message(message)
            message.ended_at = datetime.utcnow()
            message.status = MessageStatus.Done

        except:
            message.ended_at = datetime.utcnow()
            message.status = MessageStatus.Failed
            self.handle_job_failure(
                message=message
            )
            return False

        self.log.info('{0}: {1} ({2})'.format(message.origin, 'Message OK', message.id))

        return True

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        self._state = value