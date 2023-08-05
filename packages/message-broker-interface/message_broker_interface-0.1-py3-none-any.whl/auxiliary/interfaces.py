from abc import ABCMeta, abstractmethod
import socket


class GenericModule(object):
    """
    Place to store everything that all modules should have in commong:
    - analyzers
    - workers
    - etc.

    """

    @staticmethod
    def get_ip_address():
        return socket.gethostbyname(socket.gethostname())


class IProducer(GenericModule):
    """
    Gets data and sends them to the message broker
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def get_data(self, db_key, db_doc_params): raise NotImplementedError

    @abstractmethod
    def pre_validate_data(self, optional_filter): raise NotImplementedError

    @abstractmethod
    def produce_analyze_jobs(self, queue_name, queue_host, queue_port): raise NotImplementedError


class IConsumer(GenericModule):
    """
    Gets data from message broker and updates the data
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def consume_analyze_jobs(self): raise NotImplementedError
