from pathlib import Path

import oracledb

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

            print("✓ Executed")

        except oracledb.DatabaseError as e:

            error = e.args[0]

            # ORA-00955 = table already exists

            if error.code == 955:

                print("✓ Already Exists")

            else:

                raise

    conn.commit()

    cursor.close()

    conn.close()

    logger.info("Oracle schema created")


if __name__ == "__main__":

    create_schema()