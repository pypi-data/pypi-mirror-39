#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from kazoo.client import KazooClient

__name__ = "weichigong"
__version__ = '1.0.3'
__author__ = 'dashixiong'
__author_email__ = 'dashixiong.lee@gmail.com'


class zconfig:

    def __init__(self, zkHosts, app, env):
        self.app = app
        self.env = env
        self.client = KazooClient(hosts=zkHosts)
        self.client.start()

    def getPath(self, path):
        return os.path.join('/', self.app, self.env, path)

    def set(self, path, value):
        fullPath = self.getPath(path)
        self.client.ensure_path(fullPath)
        self.client.set(fullPath, value)

    def get(self, path):
        fullPath = self.getPath(path)
        return self.client.get(fullPath)[0].decode('utf-8')
