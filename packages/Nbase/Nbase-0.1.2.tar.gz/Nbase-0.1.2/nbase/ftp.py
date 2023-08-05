#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Author: 丁卫华(weihua.ding@nio.com)
#
# Created: 2018/11/15 下午6:46

from ftplib import FTP

TIMEOUT = 10


class FTPFun(object):
    """
    The FTP function object
    """
    def __init__(self, server, port, username, password, timeout=TIMEOUT):
        """

        """
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.timeout = timeout

    def login(self):
        """
        登陆FTP
        :return:
        """
        ftp_client = FTP()
        ftp_client.connect(
            host=self.server, port=int(self.port), timeout=self.timeout
        )
        ftp_client.login(self.username, self.password)
        return ftp_client
