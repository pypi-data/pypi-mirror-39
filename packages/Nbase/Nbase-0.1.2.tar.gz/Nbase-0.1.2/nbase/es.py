#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/12 下午2:30

from elasticsearch import Elasticsearch, helpers


class ESFun(object):
    """
    The ElasticSearch function object
    """
    default_id = 'id_key'
    default_doc_type = 'iris_doc'

    def __init__(self, host, username, password):
        """

        """
        self.host = host
        self.username = username
        self.password = password
        if self.host and self.username and self.password:
            self.es = Elasticsearch(
                self.host, http_auth=(self.username, self.password))

    def bulk_write(self, index, documents, id_key=default_id):
        """
        ES bulk write
        :param index:
        :param documents:
        :param id_key:
        :return:
        """
        bulk = ({
            "_index": index,
            "_type": self.default_doc_type,
            "_id": item[id_key],
            "_source": item
        } for item in documents)
        return helpers.bulk(self.es, bulk)

    # https://gist.github.com/LouisAmon/181c874ad4ee06f600f424045d508d8d
    def df_bulk_write(self, index, df_data, id_key=default_id):
        """
        Dataframe ES bulk write
        :param index:
        :param df_data:
        :param id_key:
        :return:
        """
        bulk = ({
            "_index": index,
            "_type": self.default_doc_type,
            "_id": r[id_key],
            "_source": r.to_dict()
        } for i, r in df_data.iterrows())
        return helpers.bulk(self.es, bulk)
