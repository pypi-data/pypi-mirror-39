# -*- coding: utf-8 -*-
"""
Module processor.py:
--------------------------
Provides the message processor and routing implementation and the processor Register as well.
"""
from typing import TypeVar
from .message import Message


class Register(object):
    """
    Decorator class used to register functions.

    All function registered with this class must respect the following interface:
    ``func(message:Message, *args ,**kwargs)``
    where 'message' is a 'simple_queue.Message' object containing the message received from the queue.

    This class follows the singleton pattern, ie during the entire system life cycle there is only a single
    instance of the singleton Register object.
    """
    __registry = None

    def __new__(cls):
        """
        Singleton constructor.
        """
        if cls.__registry is None:
            cls.__registry = object.__new__(cls)
            cls.__registry.registry = dict()

        return cls.__registry

    def __call__(self, title):
        """
        Register a function in the class registry.
        :param title: an string that uniquely identifies the message type.
        """

        def register(cls: TypeVar):
            """
            calls the register function.
            :param cls: a class type object.
            :return: the original class
            """
            self.register(cls, title)
            return cls

        return register

    def __getitem__(self, title: str):
        return self.registry[title]

    def __contains__(self, item):
        return item in self.registry

    def register(self, cls: TypeVar, title: str):
        """
        Register a function in the class registry.
        :param cls: a class type object.
        :param title: a string that describes the message type.
        """
        if title not in self.registry:
            handler = cls()
            if isinstance(handler, Processor):
                self.registry[title] = handler
            else:
                raise TypeError("Processors must inherits from the 'Processor' class.")

        else:
            raise KeyError("The message type {0} already has a registered Processor.".format(title))

    def set_default(self, cls: TypeVar):
        """
        Sets a default Processor which messages with no title attribute will be sent to.
        :param cls: a class type object.
        """
        handler = cls()
        if isinstance(handler, Processor):
            self.registry[None] = handler
        else:
            raise TypeError("Processors must inherits from the 'Processor' class.")


class Processor(object):
    """
    A base class for message processor.
    * `__model__` is a class attribute that provides the message body class definition 
    that will be used to parse the message.body json.
    * `__default_action__` is a class attribute that defines the name of the class default
    action to be used the the received message does not define an `message.meta["action"]` value.
    """
    __model__ = None
    __default_action__ = "run"

    def dispatch_message(self, message:Message):
        """
        Dispatch the message to the correct function based on its title.
        :param message: the `pitah_queue.message.Message` object.
        :type message: `pitah_queue.message.Message`
        """
        # get message body
        if message.body is not None and self.__model__ is not None:
            # message body parser
            message.body = self.__model__.from_json(message.body)
        # when we declare a self.__model__ then the message body must be sent within the message.
        elif message.body is None and self.__model__ is not None:
            # sanity check if message body was received when it must be sent.
            raise ValueError(
                "The messege.body attribute is required by the handler and it was not found on the message:"
                "message.title: {} \n"
                "message.id: {}\n"
                "Processor: {}".format(
                    message.title, message.id, type(self).__name__
                )
            )
        # if action exists in the handler
        # then dispatch to the action handler
        if "action" in message.kwargs:
            action = message.kwargs["action"]
        else:
            action = self.__default_action__
        if action in self:
            action = self[action]
            action(message)
        else:
            raise ValueError(
                "The Registered Processor for the `message.id` '{}' , does not implement an action named '{}'."
                "Please, Check if the message action name is correct,"
                " or check the implemented methods of the class '{}'. \n\n"
                "Message details:\n"
                "message.title: {} \n"
                "message.id: {} \n"
                "message.body: {}".format(
                    message.id, action, type(self).__name__,
                    message.title, message.id,
                    message.body
                )
            )

    def __getitem__(self, action: str):
        return getattr(self, action.lower(), None)

    def __contains__(self, item: str):
        return hasattr(self, item.lower())

    def run(self, message, *args, **kwargs):
        pass
