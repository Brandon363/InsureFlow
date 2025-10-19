import hashlib
import secrets


def hash_password(password: str) -> str:
    # Hash a password using SHA-256 with salt
    salt = secrets.token_hex(16)
    password_hash = hashlib.sha256((password + salt).encode()).hexdigest()
    return f"{salt}${password_hash}"


def verify_password(plain_password: str, hashed_password: str) -> bool:
    # Verify a password against its hash
    if hashed_password is None:
        return False

    if '$' in hashed_password:
        salt, stored_hash = hashed_password.split('$')
        new_hash = hashlib.sha256((plain_password + salt).encode()).hexdigest()
        return secrets.compare_digest(new_hash, stored_hash)

    return hash_password(plain_password) == hashed_password