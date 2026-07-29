# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import oracledb

from src.config.settings import settings


_pool = None


def get_pool():

    global _pool

    if _pool is None:

        _pool = oracledb.create_pool(

            user=settings.ORACLE_USER,

            password=settings.ORACLE_PASSWORD,

            dsn=settings.ORACLE_DSN,

            min=2,

            max=10,

            increment=1,

            getmode=oracledb.POOL_GETMODE_WAIT

        )

    return _pool


def get_connection():

    return get_pool().acquire()


def release_connection(conn):

    conn.close()