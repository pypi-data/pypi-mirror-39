#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/12 上午11:52

import json
from kafka import KafkaProducer


class KafkaFun(object):
    """The Kafka function object
    """
    def __init__(self, brokers, username, password):
        """

        :param brokers:
        :param username:
        :param password:
        """
        self.brokers = brokers
        self.username = username
        self.password = password

    def get_prd_swc(self):
        """
        获取swc Kafka的producer
        :return:
        """
        return KafkaProducer(
            bootstrap_servers=self.brokers,
            security_protocol='SASL_PLAINTEXT',
            sasl_mechanism='PLAIN',
            sasl_plain_username=self.username,
            sasl_plain_password=self.password,
            value_serializer=lambda m: json.dumps(m).encode('ascii'),
            retries=3,
            api_version_auto_timeout_ms=10000,  # 避免check_version error
        )

    def send_swc_msg(self, topic, key, value, ts=None):
        """
        给swc发送消息
        :param topic:
        :param key:
        :param value:
        :param ts:
        :return:
        """
        prd_swc = self.get_prd_swc()
        prd_swc.send(topic=topic, value=value, key=key, timestamp_ms=ts)
        prd_swc.close()
