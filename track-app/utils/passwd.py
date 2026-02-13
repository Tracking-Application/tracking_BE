# utils/password.py

import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    # Step 1: SHA256 hash (removes 72 byte limit problem)
    sha_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    # Step 2: bcrypt hash
    return pwd_context.hash(sha_hash)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    sha_hash = hashlib.sha256(plain_password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha_hash, hashed_password)
