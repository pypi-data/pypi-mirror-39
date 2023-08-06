# -*- coding: utf-8 -*-
"""
===============
Simple Queue
===============

Simple Queue is a lightweight sqs worker Queue implementation 
built upon `boto3` and pure python 3.x.

It provides a ready to use queue `Worker` implementation that dispatches 
`Messages` to `Processors`.

**Basic concepts**:

    * `Messages` bodies are defined in a declarative way extending a `MappingDefinition` class.
    * `Processor` is the processor implementation. It is the place where the user must implement \
    the functions that will handler with the received messages.
    * `Processor`s must be registered on the `Register` the `@register` directive.


Simple Examples
-----------------

:Example: Message Body Schema Definition

.. code-block:: python  
    
    from simple_mappers import MapDefinition
    from simple_mappers import properties
    
    class MetaData(MapDefinition):
        ""\"An Metadata mapping definition.
        Defines Audio MetaData inner documents.
        ""\"
        ramal = properties.StringProperty()
        other = properties.StringProperty()
    
    
    class Transcription(MapDefinition):
        ""\"A Transcription mapping definition.
        Defines audio transcription inner documents.
        ""\"
        # transcription start time in secods
        start_time = properties.IntegerProperty()
        # transcription end time in secods
        end_time = properties.IntegerProperty()
        text = properties.StringProperty()
    
    
    class Document(MapDefinition):
        ""\"A document mapping definition.
        Definition for the whole audio/transcription document.
        ""\"
        
        file_path = properties.StringProperty(
            required=True
        )
        start_date = properties.DateTimeProperty()
        end_date = properties.DateTimeProperty()
        transcription = properties.ArrayProperty(
            itens_type=Transcription
        )
        metadata = properties.ObjectProperty(
            obj_type=MetaData
        )

:Example: Processing Received Messages

.. code-block:: python 

    from pitah_queue import MessageProcessor
    from pitah_queue import Register
    from .schemas import Document as DocSchema
    from documents import AudioData
    from pitah_queue import Job
    
    # getting the registry
    registry = Register()
    
    # processors must be decorated with the registry decorator
    @registry("IndexMessage")
    class DataProcessor(MessageProcessor):
        ""\"
        A message processor class.
        ""\"
        
        __model__ = DocSchema
    
        def run(self, message: Job, *args, **kwargs):
            ""\"The function that is called to process a message received from the queue.
            The main processor function that is called by the worker when it receives a message
            entitled as IndexMessage.
            ""\"
            
            data = AudioData()
            message.body.to_object(data)
            data.save()
    
    # start the worker

.. _RabbitMQ: https://www.rabbitmq.com/
"""

from .message import Message
from .queue import Queue
from .processor import Register, Processor
from .worker import Worker, registry

__license__ = "GNU General Public License"
__author__ = "Luis Felipe Müller"
__docformat__ = 'reStructuredText'