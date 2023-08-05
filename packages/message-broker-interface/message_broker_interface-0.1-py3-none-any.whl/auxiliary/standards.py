import pika
import json
import logging

from pymongo import MongoClient
from auxiliary.interfaces import IConsumer
from auxiliary.interfaces import IProducer
from abc import abstractmethod

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class StandardProducer(IProducer):
    """
    Provides all you need to get data from a MongoDB source and process it in order to create text analyzing jobs
    and hand them over to a AMPQ server like rabbitMQ. All data will be converted to a json string which will be
    interpreted by all text analyzers on the other side.

    """

    def __init__(self, mongo_dict):
        """
        Basic initializer for all the self data.
        """
        logging.debug("StandardProducer created ...")
        self.mongo_dict = mongo_dict
        self.mongo_objects = dict()

        self.data = ""

        self.connection = ""
        self.channel = ""

    def fill_mongo_objects(self):
        """
        generate mongo objects from given parameters in mongo_dict, i.e. build connections to the relevant mongodbs
        """
        logging.debug("StandardProducer - Mongo DB Objects filled...")
        for key in self.mongo_dict:
            self.mongo_objects[key] = {}
            self.mongo_objects[key]["client"] = MongoClient(self.mongo_dict[key][0], int(self.mongo_dict[key][1]))
            self.mongo_objects[key]["mongo_db"] = self.mongo_objects[key]["client"][self.mongo_dict[key][2]]
            self.mongo_objects[key]["mongo_coll"] = self.mongo_objects[key]["mongo_db"][self.mongo_dict[key][3]]

    def get_data(self, db_key, db_doc_params):
        """
        Get data from MongoDB and save in class variable self.data

        :param db_doc_params: description how the documents of the given database are structured, i.e. which keys exist
        :return:
        """

        mongo_coll = self.mongo_objects[db_key]['mongo_coll']
        logging.debug("Mongo DB Collection <get_data>: " + str(mongo_coll))
        mongo_docs = mongo_coll.find()

        post_dicts = []
        for doc in mongo_docs:
            temp_dict = dict()
            # for each key appearing in the documents of the given database, fetch the data from the document
            for key in db_doc_params:
                temp_dict[key] = doc[key]
            post_dicts.append(json.dumps(temp_dict))

        self.data = post_dicts

    def pre_validate_data(self, optional_filter):
        """
        Can be used to outsource any data validation or manipulation before saving.

        :param optional_filter:
        :return:
        """
        pass

    def produce_analyze_jobs(self, queue_name, queue_host, queue_port):
        """
        Takes all data from self.data and puts it on a queue in the specified AMPQ server, e.g. rabbitMQ, using pika

        :param queue_name: name of the queue you want to add your jobs into
        :param queue_host: hostname or IP address from AMPQ server / rabbitMQ
        :param queue_port: port of the AMPQ server / rabbitMQ
        :return:
        """
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(queue_host, queue_port))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=queue_name)
            for data in self.data:
                logging.debug("Pushing Data to queue ( " + str(queue_name) + " ): " + str(data))
                self.channel.basic_publish(exchange='', routing_key=queue_name, body=data)
        except pika.exceptions.ConnectionClosed as exp:
            logging.debug("Connection to message broker failed: " + str(exp))

    @abstractmethod
    def register(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_db):
        raise NotImplementedError


# noinspection PyUnusedLocal
class StandardConsumer(IConsumer):
    """
    Provides some basic functions to be able to connect to any AMPQ source and get the results from the previously
    added jobs with the other TextWorkerProducer class.
    """

    def __init__(self, queue_name, queue_host, queue_port, mongo_dict):
        """
        Some basic initialization constructor

        :param queue_name: name of the queue you want to listen to on the AMPQ server
        :param queue_host: hostname or IP address of the AMPQ server you want to listen to
        :param queue_port: port of the AMPQ server you want to listen to
        :param mongo_dict: Dictionary containing the information which MongoDB need to be addressed. Possible databases
                           are "raw_data", "know_how", "cache" and "analyze" - these must be the keys in mongo_dict,
                                                                        since they will appear hardcoded in subclasses!
        """
        self.connection = ""
        self.channel = ""

        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(queue_host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name)
        self.mongo_dict = mongo_dict
        self.mongo_objects = dict()

    def fill_mongo_objects(self):
        """
        generate mongo objects from given parameters in mongo_dict, i.e. build connections to the relevant mongodbs
        """

        for key in self.mongo_dict:
            self.mongo_objects[key] = {}
            self.mongo_objects[key]["client"] = MongoClient(self.mongo_dict[key][0], int(self.mongo_dict[key][1]))
            self.mongo_objects[key]["mongo_db"] = self.mongo_objects[key]["client"][self.mongo_dict[key][2]]
            self.mongo_objects[key]["mongo_coll"] = self.mongo_objects[key]["mongo_db"][self.mongo_dict[key][3]]

    def consume_analyze_jobs(self):
        """
        Start the actual consuming process by listening to the answer queue where the analyzing systems will provide
        their solutions to the jobs.

        :return:
        """

        def callback(ch, method, properties, body):
            """
            Mandatory callback method must be included directly as a sub method from the consuming method. It will
            be get the data and add the newly generated knowledge to the original raw data (e.g. classified texts)

            self.mongo_coll.insert_one(whatever)

            :param ch: will not be used but is mandatory according to pika tutorials
            :param method: will not be used but is mandatory according to pika tutorials
            :param properties: will not be used but is mandatory according to pika tutorials
            :param body: represents the data came from AMPQ
            :return:
            """
            return body

        self.channel.basic_consume(callback,
                                   queue=self.queue_name,
                                   no_ack=True)

        self.channel.start_consuming()

    @abstractmethod
    def register(self, mysql_host, mysql_port, mysql_user, mysql_password, mysql_db): raise NotImplementedError
