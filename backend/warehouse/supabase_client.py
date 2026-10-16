"""Lazy Supabase client construction with explicit configuration errors."""
from functools import lru_cache
from supabase import Client, create_client
from src.config.settings import settings

@lru_cache(maxsize=1)
def get_supabase() -> Client:
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        raise RuntimeError("SUPABASE_URL and SUPABASE_KEY must be set in backend/.env")
    return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)

# Compatibility for older modules that import the module-level `supabase` object.
class _LazySupabaseProxy:
    def __getattr__(self, name):
        return getattr(get_supabase(), name)

supabase = _LazySupabaseProxy()
