from auxiliary.standards import StandardProducer
from auxiliary.standards import StandardConsumer

import gridfs
import base64


class ObjectWorkerProducer(StandardProducer):
    """
    This class provides methods to fetch fresh videos and images from raw data mongodb and put them into RabbitMQ
    for further processing with video / image analysis tools, e.g. object detection
    """

    def __init__(self, mongo_dict):
        """
        :param mongo_dict: dictionary containing the information about
        """
        super(ObjectWorkerProducer, self).__init__(mongo_dict)
        self.fill_mongo_objects()

    def get_data(self, db_key, db_doc_params=None):
        """
        This method overrides the get_data method of the standard producer.
        It retrieves data from raw_db, i.e. images or videos and converts them into base64 hashes in order to
        put them into rabbitmq for further processing with analyzers
        db_doc_params for images/vids given by gridfs: ['_id', 'md5', 'chunksize', 'length', 'uploadDate']
        -> the most important is '_id' such that the image/video can be retrieved and then converted into a base64 hash
        which later can be passed to rabbitmq
        :param db_key: which db is connected to, i.e. raw_db in most cases
        :param db_doc_params: how is this db structured, i.e. which key names do exist in documents of this db

        db_doc_params: not necessary because of fetching the data via gridfs!
        """
        # connect to mongo_db via gridfs and get all image/video docs
        mongo_db = self.mongo_objects[db_key]['mongo_db']
        fs = gridfs.GridFS(mongo_db)
        file_hash_list = list()
        file_docs = fs.find()
        # compute the base64 hash of each file
        for im in file_docs:
            im_hash = base64.b64encode(im)
            file_hash_list.append(im_hash)
        # set self.data to the list of file hashes, such this can be put into rabbitmq via pika
        self.data = file_hash_list


class ObjectWorkerConsumer(StandardConsumer):
    """
    This class provides methods for listeting to the RabbitMQ answer queue for results of image /video analysis methods,
    such that the results can be imported into the analysis database or queued for further analysing steps
    """

    def __init__(self, queue_name, queue_host, queue_port, mongo_dict):
        super(ObjectWorkerConsumer, self).__init__(queue_name, queue_host, queue_port, mongo_dict)
        self.fill_mongo_objects()

    def consume_analyze_jobs(self):
        """
        Start the consuming process by listening to the answer queue where the analyzing modules will provide
        their results and transfer the results for further processing or store them in analyzer mongodb
        """
        mongo_objects = self.mongo_objects
        image_bool = ("image" in self.queue_name)

        def callback(ch, method, properties, body):
            """
                Mandatory callback method must be included directly as a sub method from the consuming method. It will
                be get the data and add the newly generated knowledge to the original raw data (e.g. classified texts)

                self.mongo_coll.insert_one(whatever)

                :param ch: will not be used but is mandatory according to pika tutorials
                :param method: will not be used but is mandatory according to pika tutorials
                :param properties: will not be used but is mandatory according to pika tutorials
                :param body: represents the data came from AMPQ
            """

            # get test data from rabbitmq queue
            analyzed = body.decode('utf-8').replace("'", '"')
            # rebuild the actual image from base64 hash
            temp_file = base64.b64decode(analyzed)
            temp_result = ""
            if image_bool:
                temp_result = "temp_pic.jpg"
            else:
                temp_result = "temp_vid.mp4"
            # store actual file in temporary file
            with open(temp_result, 'wb') as f_out:
                f_out.write(temp_file)
            # connect to mongodb via gridfs
            db = mongo_objects['analyze']['mongo_db']
            fs = gridfs.GridFS(db)
            # store the file in analyze db
            fs.put(open(temp_result, 'rb'))

        self.channel.basic_consume(callback,
                                   queue=self.queue_name,
                                   no_ack=True)

        self.channel.start_consuming()
