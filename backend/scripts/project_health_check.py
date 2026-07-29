# -------------------------------------------------------------------
# Copyright (c) 2026 Ved Talmaley. All Rights Reserved.
# This project and its source code are strictly proprietary.
# Unauthorized copying, distribution, or use is strictly prohibited.
# -------------------------------------------------------------------

import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

import importlib

print("=" * 60)
print("QUANTUMLENS PROJECT HEALTH CHECK")
print("=" * 60)



checks = []


def check(name, func):
    try:
        func()
        checks.append((name, True))
        print(f"✅ {name}")
    except Exception as e:
        checks.append((name, False))
        print(f"❌ {name}")
        print(f"   {type(e).__name__}: {e}")


# ---------------------------------------------------
# Folder Structure
# ---------------------------------------------------

def folders():
    required = [
        "data/raw",
        "data/generated",
        "data/vectordb",
        "warehouse",
        "src/api",
        "src/rag",
        "src/ingestion",
        "src/transformation",
    ]

    for f in required:
        if not Path(f).exists():
            raise Exception(f"Missing {f}")


# ---------------------------------------------------
# Config
# ---------------------------------------------------

def settings():
    from src.config.settings import settings

    assert settings.ORACLE_USER
    assert settings.ORACLE_PASSWORD
    assert settings.ORACLE_DSN


# ---------------------------------------------------
# Oracle
# ---------------------------------------------------

def oracle():
    from warehouse.oracle_client import get_connection

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("select 'OK' from dual")

    assert cur.fetchone()[0] == "OK"

    cur.close()
    conn.close()


# ---------------------------------------------------
# Metrics Table
# ---------------------------------------------------

def metrics_table():
    from warehouse.oracle_client import get_connection

    conn = get_connection()

    cur = conn.cursor()

    cur.execute("select count(*) from metrics")

    rows = cur.fetchone()[0]

    if rows == 0:
        raise Exception("Metrics table empty")

    print(f"   Rows: {rows}")

    cur.close()
    conn.close()


# ---------------------------------------------------
# SQL Retriever
# ---------------------------------------------------

def sql():
    from src.rag.sql_retriever import SQLRetriever

    retriever = SQLRetriever()

    data = retriever.get_metric("net_interest_income")

    if len(data) == 0:
        raise Exception("No metric returned")


# ---------------------------------------------------
# ChromaDB
# ---------------------------------------------------

def chroma():
    from src.rag.vector_loader import load_vector_db

    db = load_vector_db()

    if db is None:
        raise Exception("Vector DB not loaded")


# ---------------------------------------------------
# Embeddings
# ---------------------------------------------------

def embeddings():
    p = Path("data/generated/embeddings.json")

    if not p.exists():
        raise Exception("embeddings.json missing")


# ---------------------------------------------------
# KPI Records
# ---------------------------------------------------

def kpis():
    p = Path("data/generated/kpi_records.json")

    if not p.exists():
        raise Exception("kpi_records.json missing")


# ---------------------------------------------------
# FastAPI
# ---------------------------------------------------

def api():
    import src.api.main


# ---------------------------------------------------
# Execute
# ---------------------------------------------------

check("Folder Structure", folders)
check("Settings", settings)
check("Oracle Connection", oracle)
check("Metrics Table", metrics_table)
check("SQL Retriever", sql)
check("Embeddings", embeddings)
check("KPI Records", kpis)
check("ChromaDB", chroma)
check("FastAPI Import", api)

print("\n" + "=" * 60)

passed = sum(x[1] for x in checks)
failed = len(checks) - passed

print(f"Passed : {passed}")
print(f"Failed : {failed}")

print("=" * 60)