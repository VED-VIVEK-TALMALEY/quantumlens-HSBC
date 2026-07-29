from supabase import Client, create_client

from src.config.settings import settings

# --------------------------------------------------
# Shared Supabase Client
# --------------------------------------------------

supabase: Client = create_client(
    settings.SUPABASE_URL,
    settings.SUPABASE_KEY
)


def get_supabase() -> Client:
    return supabase