import argparse
import sys

from auxiliary.standards import StandardConsumer
from auxiliary.standards import StandardProducer


class TextAnalyzeProduce(StandardProducer):
    pass


class TextAnalyzeConsume(StandardConsumer):
    pass


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

    # get data from mongodb
    parser.add_argument('--host', action='store', help="IP Address of MongoDB Host")
    parser.add_argument('--port', action='store', help='Port of the MongoDB Server', default=27017)
    parser.add_argument('--dbname', action='store', help='Name of the MongoDB in which the data can be found')
    parser.add_argument('--collectionname', action='store', help='Name of the collection in MongoDB',
                        default='raw_data')

    # rabbitmq params
    parser.add_argument('--queuename',
                        action='store',
                        help='Queue name on rabbitMQ server where there is another module listening')
    parser.add_argument('--queuehost', action='store', help='Hostname of the rabbitMQ server or IP address')
    parser.add_argument('--queueport', action='store', help='Port of the rabbitMQ server', default=15672)

    args = parser.parse_args(sys.argv[1:])

    if args.consumejobs:
        twp = TextAnalyzeProduce()
        twp.get_data(str(args.host), str(args.port), str(args.dbname), str(args.collectionname))
        twp.produce_analyze_jobs(str(args.queuename), str(args.queuehost), str(args.queueport))

    else:
        twc = TextAnalyzeConsume()
        twc.consume_analyze_jobs(str(args.queuename), str(args.queuehost), str(args.queueport))


if __name__ == "__main__":
    main()
