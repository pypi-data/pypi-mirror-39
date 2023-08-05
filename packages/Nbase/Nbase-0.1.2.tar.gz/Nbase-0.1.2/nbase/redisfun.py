#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/12 下午1:57

import redis
from rediscluster import StrictRedisCluster


class RedisFun(object):
    """The Redis function object
    """
    def __init__(self, cluster_nodes, cluster_password,
                 server=None, port=None, password=None):
        """
        Redis cluster client & redis server client
        :param cluster_nodes:
        :param cluster_password:
        :param server:
        :param port:
        :param password:
        """
        self.cluster_nodes = cluster_nodes
        self.cluster_password = cluster_password
        self.server = server
        self.port = port
        self.password = password
        self.r_client = self.get_redis_client()
        self.rc_client = self.get_redis_cluster_client()

    def get_redis_client(self):
        """
        Return a Redis client object
        :return:
        """
        if self.server and self.port and self.password:
            return redis.StrictRedis(
                host=self.server, port=self.port, password=self.password, db=0)
        return None

    def get_redis_cluster_client(self):
        """
        Return a Redis cluster client object
        :return:
        """
        if self.cluster_nodes and self.cluster_password:
            return StrictRedisCluster(
                startup_nodes=self.cluster_nodes,
                decode_responses=True,
                password=self.cluster_password
            )
        return None

    def set_value(self, key, value, ex=None):
        """
        写value
        :param key:
        :param value:
        :param ex:
        :return:
        """
        return self.r_client.set(key, value, ex=ex)

    def get_value(self, key):
        """
        读value
        :param key:
        :return:
        """
        return self.r_client.get(key)

    def rc_set_value(self, key, value, ex=None):
        """
        写value
        :param key:
        :param value:
        :param ex:
        :return:
        """
        return self.rc_client.set(key, value, ex=ex)

    def rc_get_value(self, key):
        """
        读value
        :param key:
        :return:
        """
        return self.rc_client.get(key)
