import streamlit as st
import httpx
from urllib.parse import urlparse


from supabase import create_client, Client


class DatabaseConfigError(RuntimeError):
    pass


class DatabaseConnectionError(RuntimeError):
    def __init__(self, operation, message):
        self.operation = operation
        super().__init__(f"{operation} failed: {message}")


def _get_required_secret(name):
    try:
        value = st.secrets[name]
    except Exception as exc:
        raise DatabaseConfigError(f"Missing {name} in .streamlit/secrets.toml") from exc

    value = str(value).strip()
    if not value:
        raise DatabaseConfigError(f"{name} is empty in .streamlit/secrets.toml")
    return value


def _get_supabase_url():
    url = _get_required_secret("SUPABASE_URL")
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise DatabaseConfigError("SUPABASE_URL must be a full URL like https://your-project.supabase.co")
    return url


def execute_supabase(query, operation="Database request"):
    try:
        return query.execute()
    except httpx.ConnectError as exc:
        raise DatabaseConnectionError(
            operation,
            "could not reach Supabase. Check your internet connection, DNS, and SUPABASE_URL.",
        ) from exc
    except httpx.TimeoutException as exc:
        raise DatabaseConnectionError(
            operation,
            "timed out while waiting for Supabase.",
        ) from exc
    except httpx.NetworkError as exc:
        raise DatabaseConnectionError(
            operation,
            "network access to Supabase failed.",
        ) from exc
    except httpx.HTTPError as exc:
        raise DatabaseConnectionError(
            operation,
            "Supabase returned an HTTP client error.",
        ) from exc


_supabase_client: Client | None = None


def get_supabase_client():
    global _supabase_client
    if _supabase_client is None:
        try:
            _supabase_client = create_client(
                _get_supabase_url(),
                _get_required_secret("SUPABASE_KEY"),
            )
        except DatabaseConfigError:
            raise
        except Exception as exc:
            raise DatabaseConfigError(f"Could not initialize Supabase client: {exc}") from exc
    return _supabase_client


class SupabaseClientProxy:
    def __getattr__(self, name):
        return getattr(get_supabase_client(), name)


supabase = SupabaseClientProxy()
