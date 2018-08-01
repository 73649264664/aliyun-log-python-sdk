#!/usr/bin/env python
# encoding: utf-8

# Copyright (C) Alibaba Cloud Computing
# All rights reserved.


import logging
import os
import sys

from aliyun.log.es_migration import MigrationManager

logger = logging.getLogger()
logger.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
logger.addHandler(ch)


def main():
    migration_manager = MigrationManager(hosts="elastic:elastic@localhost:9200",
                                         indexes="all_data_types*",
                                         scroll="2m",
                                         endpoint=os.getenv("endpoint"),
                                         project_name=os.getenv("project_name"),
                                         access_key_id=os.getenv("access_key_id"),
                                         access_key=os.getenv("access_key"),
                                         pool_size=24,
                                         time_reference="es_date",
                                         source="my_source",
                                         topic="my_topic",
                                         wait_time_in_secs=60)
    res = migration_manager.migrate()
    print res


if __name__ == "__main__":
    main()
