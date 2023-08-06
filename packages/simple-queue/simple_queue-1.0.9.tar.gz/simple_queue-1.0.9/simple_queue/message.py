# -*- coding: utf-8 -*-
"""
Module message.py:
--------------------------
    Provides the underlying structure class of an Pitah Queue Message.
"""
from uuid import uuid4
from . import utils
from datetime import datetime
from simple_mappers import MapDefinition
from enum import Enum


class MessageStatus(Enum):
    """
    Enum of worker possible status.
    """
    Processing = 'Processing'
    Enqueued = 'Enqueued'
    Done = 'Done'
    Failed = 'Failed'


class Message(object):
    """
    A Message is just a convenient data structure to pass around message (meta) data.
    """

    # Message construction
    @classmethod
    def create(cls, title, body:MapDefinition, description=None,
               _id=None, origin=None, kwargs=None):
        """
        A message builder function.
        :param title: The message title. The message title is used to route messages to its processors.
        :param body: The message body content object.
        :type body: MapDefinition
        :param kwargs: Any additional message named attribute to be included.
        :param description: A description to the message.
        :param _id: The message id.
        :param origin: The message Queue name that the message belongs to.
        :return: an Message object.
        """

        message = cls()

        if _id is not None:
            message.id = _id

        if origin is not None:
            message.origin = origin

        # Set the core job tuple properties
        if isinstance(title, str):
            message.title = title
        else:
            raise TypeError('Expected a string, but got: {0}'.format(title))

        message.body = body

        if kwargs is None:
            kwargs = dict()
        message.kwargs = kwargs

        # Extra meta data
        message.description = description

        return message

    def __init__(self, _id=None):
        """
        Message initializer function.
        :param _id: An message Id.
        """
        if _id is None:
            self.id = str(uuid4())
        else:
            self.id = _id
        self.created_at = datetime.utcnow()
        self.title = None
        self.body = None
        self.kwargs = None

        self.description = None
        self.origin = None
        self.enqueued_at = None
        self.started_at = None
        self.ended_at = None
        self.result = None
        self.exc_info = None
        self.status = None
        # the original message object
        self._msg = None

    @classmethod
    def from_queue(cls, obj):  # noqa
        """Parses a message object received from the queue.
        """
        def to_date(date_str):
            if date_str is None:
                return
            else:
                return utils.utcparse(str(date_str))

        msg = cls()
        msg._msg = obj
        msg.body = obj.body
        if obj.message_attributes is not None:
            msg.created_at = to_date(obj.message_attributes.pop('created_at',{}).get('StringValue'))
            msg.origin = obj.message_attributes.pop('origin', {}).get('StringValue')
            msg.description = obj.message_attributes.pop('description', {}).get('StringValue')
            msg.enqueued_at = to_date(obj.message_attributes.pop('enqueued_at', {}).get('StringValue'))
            msg.title = obj.message_attributes.pop("title",{}).get('StringValue')
            msg.id = obj.message_attributes.pop("Id", {}).get('StringValue')
            # parse the remaining attributes
            msg.kwargs = dict()
            for name, attrib in obj.message_attributes.items():
                msg.kwargs[name] = attrib.get("StringValue")
        else:
            msg.kwargs = dict()

        return msg

    def to_dict(self):
        """
        Returns a serialization of the current message instance.
        """
        attributes = dict()
        attributes['created_at'] = {
            'DataType': 'String',
            'StringValue': utils.utcformat(self.created_at or datetime.utcnow())
        }
        attributes["Id"] = {
                'DataType': 'String',
                'StringValue': self.id
            }
        if self.origin is not None:
            attributes['origin'] = {
                'DataType': 'String',
                'StringValue': self.origin
            }

        if self.description is not None:
            attributes['description'] = {
                'DataType':'String',
                'StringValue': self.description
            }

        if self.enqueued_at is not None:
            attributes['enqueued_at'] = {
                'DataType':'String',
                'StringValue': utils.utcformat(self.enqueued_at)
            }

        if self.title is not None:
            attributes['title'] = {
                'DataType': 'String',
                'StringValue': self.title
            }

        # parse kwargs to message attributes
        for name, value in self.kwargs.items():
            attributes[name] = {
                'DataType': 'String',
                'StringValue': str(value)
            }

        # builds the message dictionary
        obj = {
            "MessageAttributes":attributes,
            "MessageBody": self.body.to_json()
        }
        return obj

    def ok(self):
        self._msg.delete()