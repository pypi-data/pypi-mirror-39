#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/9 下午7:12

from flask import Config, helpers

from .mongofun import MongoFun
from .redisfun import RedisFun
from .kafkafun import KafkaFun
from .es import ESFun
from .ftp import FTPFun
from .s3 import S3Fun


class Nbase(object):
    """The Nbase object
    Usually you create a :class:`Nbase` instance in your main module or
    in the :file:`__init__.py` file of your package like this::

        from nbase import Nbase
        app = Nbase(__name__)
    """
    # Mongo module used for MongoDB API.
    mongo_class = MongoFun

    # Redis module
    redis_class = RedisFun

    # Kafka module for sending/receiving message
    kafka_class = KafkaFun

    # Elasticsearch module
    es_class = ESFun

    # FTP module
    ftp_class = FTPFun

    # S3 module
    s3_class = S3Fun

    def __init__(self, import_name, config_file):
        """

        :param import_name:
        :param config_file:
        """
        self.import_name = import_name
        root_path = helpers.get_root_path(self.import_name)
        self.config = Config(root_path)
        self.config.from_pyfile(config_file)

        # Make Kafka client object. This method loads Kafka configs
        # from self.config.
        self.redisfun = self.make_redis_client()

        # Make Kafka client object. This method loads Kafka configs
        # from self.config.
        self.kafkafun = self.make_kafka_client()

        # Make Elasticsearch client object. This method loads ES configs
        # from self.config.
        self.es = self.make_es_client()

        # Make FTP client object. This method loads FTP configs
        # from self.config.
        self.ftp = self.make_ftp_client()

        # Make S3 client object. This method loads S3 configs
        # from self.config.
        self.s3 = self.make_s3_client()

    def make_redis_client(self):
        """
        Used to create the RedisFun client object
        :return:
        """
        return self.redis_class(
            self.config.get('REDIS_CLUSTER_NODES', None),
            self.config.get('REDIS_CLUSTER_PASSWORD', None),
            self.config.get('REDIS_SERVER', None),
            self.config.get('REDIS_PORT', None),
            self.config.get('REDIS_PASSWORD', None)
        )

    def make_kafka_client(self):
        """
        Used to create the KafkaFun client object
        :return:
        """
        return self.kafka_class(
            self.config.get('KAFKA_BROKERS_SWC', None),
            self.config.get('KAFKA_USERNAME', None),
            self.config.get('KAFKA_PASSWORD', None)
        )

    def make_es_client(self):
        """
        Used to create the Elasticsearch client object
        :return:
        """
        return self.es_class(
            self.config.get('ES_HOST', None),
            self.config.get('ES_USERNAME', None),
            self.config.get('ES_PASSWORD', None)
        )

    def make_ftp_client(self):
        """
        Used to create the FTP client object
        :return:
        """
        return self.ftp_class(
            self.config.get('FTP_SERVER', None),
            self.config.get('FTP_PORT', None),
            self.config.get('FTP_USERNAME', None),
            self.config.get('FTP_PASSWORD', None),
            self.config.get('FTP_TIMEOUT', None)
        )

    def make_s3_client(self):
        """
        Used to create the S3 client object
        :return:
        """
        return self.s3_class(
            self.config.get('S3_REGION', None),
            self.config.get('S3_ACCESS_KEY_ID', None),
            self.config.get('S3_SECRET_ACCESS_KEY', None),
            self.config.get('S3_BUCKET', None)
        )
