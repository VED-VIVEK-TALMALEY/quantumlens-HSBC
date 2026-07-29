# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------
import sys
from pathlib import Path

import oracledb

# Add backend directory to sys.path to resolve imports correctly
backend_dir = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(backend_dir))

from src.utils.logger import logger
from warehouse.oracle_client import get_connection

BASE_DIR = Path(__file__).resolve().parent


def create_schema():

    conn = get_connection()

    cursor = conn.cursor()

    schema_file = BASE_DIR / "schema.sql"

    sql = schema_file.read_text(encoding="utf-8")

    statements = [
        stmt.strip()
        for stmt in sql.split(";")
        if stmt.strip()
    ]

    for statement in statements:

        try:

            cursor.execute(statement)

            print("[OK] Executed")

        except oracledb.DatabaseError as e:

            error = e.args[0]

            # ORA-00955 = table already exists

            if error.code == 955:

                print("[OK] Already Exists")

            else:

                raise

    conn.commit()

    cursor.close()

    conn.close()

    logger.info("Oracle schema created")


if __name__ == "__main__":

    create_schema()