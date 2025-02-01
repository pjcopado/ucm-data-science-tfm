from slowapi import Limiter
from slowapi.util import get_remote_address

from src.app.core.config import settings

limiter = Limiter(
    key_func=get_remote_address,
    strategy="fixed-window",
    storage_uri="memory://",
    default_limits=["2/minute"],
    enabled=settings.RATE_LIMIT_ENABLED,
)
