#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Alibaba Cloud Computing
# All rights reserved.

import json
import re
import string

from aliyun.log.es_migration.util import split_and_strip


class LogstoreRegex(object):

    def __init__(self, logstore, regex=None):
        self.logstore = logstore
        self.regex = regex


class LogstoreIndexMapper(object):

    def __init__(self, logstore_index_mappings):
        d = json.loads(logstore_index_mappings)
        self._build_index_logstore_map(d)

    def _build_index_logstore_map(self, d):
        self.index_logstore_map = {}
        for k, v in d.iteritems():
            indexes = split_and_strip(v, ",")
            for index in indexes:
                if string.find(index, "*") != -1:
                    regex = re.compile(string.replace(index, "*", ".*"))
                    self.index_logstore_map[index] = LogstoreRegex(k, regex)
                else:
                    self.index_logstore_map[index] = LogstoreRegex(k)

    def get_logstore(self, index):
        if index in self.index_logstore_map:
            return self.index_logstore_map[index].logstore
        for k, v in self.index_logstore_map.iteritems():
            if string.find(k, "*") == -1:
                continue
            if re.match(v.regex, index):
                self.index_logstore_map[index] = v
                return v.logstore
        return None
