# -*- coding: utf-8 -*-
"""
Module queue.py:
--------------------------
A simple Queue client that is used to send messages to the queue.
"""
from .message import Message, MessageStatus
from datetime import datetime
import json


class Queue(object):
    """
    A simple Queue class that provides simple ways to send messages to the message queue.
    """
    def __init__(self, queue_name, sqs, dl_queue=None, max_receive_count=10,
                 message_wait_time=20, visibility_timeout=60):
        """Queue initialization function.
        :param queue_name: A queue name.
        :param sqs: A boto3 sqs Resource.
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
        self.queue_name = queue_name
        self.dl_queue_name = dl_queue
        self.max_receive_count = max_receive_count
        self.message_wait_time = message_wait_time
        self.visibility_timeout = visibility_timeout
        self._init_queues()

    def _init_queues(self):
        """
        Queue Resource Initialization.
        """
        self.queue = self._get_or_create_queue(self.queue_name)
        if self.dl_queue_name is not None:
            self.dl_queue = self._get_or_create_queue(self.dl_queue_name)

            # checking queue dead letter configuration
            if (
                    "RedrivePolicy" not in self.queue.attributes or
                    self.get_redrive_policy().get('deadLetterTargetArn') != self.dl_queue.attributes["QueueArn"]
            ):
                redrive_policy = {
                    # 'deadLetterTargetArn': self.dl_queue.attributes["QueueArn"],
                    'deadLetterTargetArn': self.dl_queue.attributes["QueueArn"],
                    'maxReceiveCount': str(self.max_receive_count)
                }
                # Configure queue to send messages to dead letter queue
                response = self.queue.set_attributes(
                    Attributes={
                        'RedrivePolicy': json.dumps(redrive_policy),
                    }
                )

    def _get_or_create_queue(self, name):
        """
        Gets or creates a new queue with the identifier received as parameter.
        :param name: The queue name identifier
        :return: the created or recovered resource.
        """
        try:
            return self.sqs.get_queue_by_name(QueueName=name)
        except self.client.exceptions.QueueDoesNotExist as ex:
            queue = self.sqs.create_queue(
                QueueName=name,
                Attributes={
                    'DelaySeconds': '5',
                    'ReceiveMessageWaitTimeSeconds': str(self.message_wait_time),
                    "VisibilityTimeout": str(self.visibility_timeout)
                }
            )
            return queue

    def get_redrive_policy(self):
        redrive_policy = self.queue.attributes.get("RedrivePolicy", None)
        if isinstance(redrive_policy, str):
            return json.loads(redrive_policy)
        else:
            return redrive_policy

    def enqueue(self, title, body, **kwargs):
        """Creates a message instance and enqueues it.
        :param title: the message title.
        :param body: a message body object.
        :type body: MappingDefinition.
        :param description: A message description string.
        **Default**: None
        :param _id: The message ID. **Default**: None auto-generated id;
        """
        description = kwargs.pop('description', None)
        _id = kwargs.pop('_id', None)

        msg = Message.create(
            title=title,
            body=body,
            description=description,
            _id=_id,
            origin=self.queue_name,
            kwargs=kwargs
        )
        msg.enqueued_at = datetime.utcnow()
        # message serialization
        response = self.queue.send_message(
            **msg.to_dict()
        )

        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
            raise Exception(
                "Message following message could not be delivered.\n"
                "Execution Details:\n"
                "message.title: {} \n"
                "message.body: {} \n"
                "queue_name: {}".format(title, body.to_json(), self.queue_name)
            )
        msg.status = MessageStatus.Enqueued
        msg._msg = response
        return msg

    def receive_messages(self):
        for msg in self.queue.receive_messages(MessageAttributeNames=['All'], WaitTimeSeconds=5):
            message = Message.from_queue(msg)
            yield message
        # sequence of messages aways ends with a None
        yield None
