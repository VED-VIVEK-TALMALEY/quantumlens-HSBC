"""Supabase-based QuantumLens health check. Run from backend: python scripts/project_health_check.py"""
import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

checks = []
def check(name, fn):
    try:
        result = fn()
        checks.append((name, True))
        print(f"[OK] {name}" + (f": {result}" if result is not None else ""))
    except Exception as exc:
        checks.append((name, False))
        print(f"[FAIL] {name}: {type(exc).__name__}: {exc}")

def folders():
    required = ["data/raw", "data/generated", "data/vectordb", "warehouse", "src/api", "src/rag", "src/ingestion", "src/transformation"]
    missing = [item for item in required if not (BASE_DIR / item).exists()]
    if missing: raise RuntimeError("Missing directories: " + ", ".join(missing))
    return "required directories present"

def settings_check():
    from src.config.settings import settings
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL/SUPABASE_KEY missing; check backend/.env")
    return "Supabase URL and key configured"

def supabase_check():
    from warehouse.supabase_client import get_supabase
    response = get_supabase().table("metrics").select("id", count="exact").limit(1).execute()
    return f"connected; total rows={response.count if response.count is not None else 'unknown'}"

def api_check():
    from src.api.main import app
    return f"FastAPI app imported ({app.title})"

def embedding_client_check():
    from src.config.settings import settings
    return settings.EMBEDDING_SERVICE_URL

check("Folders", folders)
check("Settings", settings_check)
check("Supabase connectivity", supabase_check)
check("Embedding service URL", embedding_client_check)
check("FastAPI import", api_check)
passed = sum(ok for _, ok in checks)
failed = len(checks) - passed
print(f"\nHealth checks: {passed} passed, {failed} failed")
raise SystemExit(1 if failed else 0)
