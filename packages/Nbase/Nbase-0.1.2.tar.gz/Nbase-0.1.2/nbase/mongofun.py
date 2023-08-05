#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/9 下午7:39

from pymongo import MongoClient, ReadPreference


READ_SLAVE = ReadPreference.SECONDARY_PREFERRED
READ_PRIMARY = ReadPreference.PRIMARY


class MongoFun(object):
    """The MongoDB function object
    """
    def __init__(self, mongo_uri):
        self.mongo_uri = mongo_uri

    def get_fellow_mongo_conn(self):
        """
        获取nio_fellow的MongoClient
        :return:
        """
        return MongoClient(self.mongo_uri)

    def get_fellow_mongo_collection(self, collection_name, is_read_slave):
        """
        获取collection
        :param collection_name:
        :param is_read_slave: 读写分离salve
        :return:
        """
        db = self.get_fellow_mongo_conn().get_database()
        if is_read_slave:
            return db.get_collection(
                collection_name, read_preference=READ_SLAVE)
        return db.get_collection(collection_name)
