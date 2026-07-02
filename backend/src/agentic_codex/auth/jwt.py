from datetime import datetime, timedelta, timezone
from jose import jwt
import os
import time

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def _get_secret_key() -> str:
    secret_key = os.getenv("JWT_SECRET")
    if not secret_key:
        raise RuntimeError("JWT_SECRET environment variable must be set")
    return secret_key


def create_access_token(data: dict):
    to_encode = data.copy()

    # JWT spec requires `exp` as a numeric timestamp (epoch seconds)
    exp_ts = int(time.time() + ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    to_encode.update({"exp": exp_ts})

    return jwt.encode(
        to_encode,
        _get_secret_key(),
        algorithm=ALGORITHM
    )