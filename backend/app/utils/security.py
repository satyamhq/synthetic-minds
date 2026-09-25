"""
Security utilities for Synthetic Minds.
Provides path traversal prevention, safe identifier validation, and secure error payload formatting.
"""
import os
import re
import traceback
from typing import Optional, Any, Dict
from ..config import Config

SAFE_ID_PATTERN = re.compile(r'^[a-zA-Z0-9_\-]{1,128}$')


def is_safe_id(id_str: Any) -> bool:
    """Check if identifier consists solely of safe characters without traversal tokens."""
    if not id_str or not isinstance(id_str, str):
        return False
    if '..' in id_str or '/' in id_str or '\\' in id_str or '\x00' in id_str:
        return False
    return bool(SAFE_ID_PATTERN.match(id_str))


def safe_join_path(base_dir: str, *subpaths: str) -> str:
    """
    Safely join subpaths to a base directory, verifying the result stays within base_dir.
    Raises ValueError if path traversal is detected.
    """
    base = os.path.abspath(base_dir)
    joined = os.path.abspath(os.path.join(base, *subpaths))
    if not (joined == base or joined.startswith(base + os.sep)):
        raise ValueError(f"Path traversal detected: {subpaths}")
    return joined


def format_error_payload(message: str, exc: Optional[Exception] = None, **extra: Any) -> Dict[str, Any]:
    """
    Construct standardized JSON error response.
    Never exposes internal tracebacks unless Config.DEBUG is explicitly enabled.
    """
    payload = {
        "success": False,
        "error": message
    }
    if Config.DEBUG and exc:
        payload["traceback"] = traceback.format_exc()
    payload.update(extra)
    return payload
