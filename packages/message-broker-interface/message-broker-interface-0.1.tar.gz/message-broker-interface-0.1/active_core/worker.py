import argparse

from auxiliary.standards import StandardConsumer
from auxiliary.standards import StandardProducer
from auxiliary.utils import parse_mongo_dict
import logging
import json

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")


class TextWorkerProducer(StandardProducer):

    def __init__(self, mongo_dict):
        logging.debug("TextWorkerProducer generated ...")
        super(TextWorkerProducer, self).__init__(mongo_dict)
        self.fill_mongo_objects()


class TextWorkerConsume(StandardConsumer):

    def __init__(self, queue_name, queue_host, queue_port, mongo_dict):
        super(TextWorkerConsume, self).__init__(queue_name, queue_host, queue_port, mongo_dict)
        self.fill_mongo_objects()

    def consume_analyze_jobs(self):
        """
        Start the actual consuming process by listening to the answer queue where the analyzing systems will provide
        their solutions to the jobs.

        :return:
        """
        mongo_objects = self.mongo_objects

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
            # get test data from rabbitmq queue
            myjson = body.decode('utf-8').replace("'", '"')
            analyzed = json.loads(myjson)  # json_object for the current document in rabbitmq
            # add the results to the dict and import it into cache mongodb
            mongo_objects['analyze']['mongo_coll'].insert_one(analyzed)

        self.channel.basic_consume(callback,
                                   queue=self.queue_name,
                                   no_ack=True)

        self.channel.start_consuming()


def main():
    """
    General hook method for the program to start within a function and not functionless.

    :return:
    """
    parser = argparse.ArgumentParser()

    # main switch (consume or produce)
    parser.add_argument('--consumejobs',
                        action='store_true',
                        help="Set if you want to consume jobs, otherwise the producer will be started",
                        default=False)

    # rabbitmq params
    parser.add_argument('--queuename',
                        action='store',
                        help='Queue name on rabbitMQ server where there is another module listening.')
    parser.add_argument('--queuehost', action='store', help='Hostname of the rabbitMQ server or IP address')
    parser.add_argument('--queueport', action='store', help='Port of the rabbitMQ server', default=15672)

    parser.add_argument("--mdata", dest="mongo_dict", action='append', required=True)

    args = parser.parse_args()

    mongo_dict = parse_mongo_dict(args)
    logging.debug("Mongo DB - Dictionary: " + str(mongo_dict))

    if args.consumejobs:
        twc = TextWorkerConsume(str(args.queuename), str(args.queuehost), str(args.queueport), mongo_dict)
        twc.consume_analyze_jobs()

    else:
        logging.debug("Producing detected ...")
        db_doc_params = ['_id', 'text', 'label', 'identityhash']
        twp = TextWorkerProducer(mongo_dict)

        twp.get_data('raw_data', db_doc_params)
        twp.produce_analyze_jobs(str(args.queuename), str(args.queuehost), int(args.queueport))


if __name__ == "__main__":
    main()
