from argon2 import PasswordHasher

# Configure Argon2id parameters to meet modern enterprise standards (Slide 5)
# m=65536 memory cost (64MB), t=3 time iterations, p=1 parallelism thread
ph = PasswordHasher(memory_cost=65536, time_cost=3, parallelism=1)

def hash_password(password: str) -> str:
    """Takes a plain text password and returns a secure irreversible hash."""
    return ph.hash(password)

def verify_password(hashed_password: str, plain_password: str) -> bool:
    """Verifies a plain text password against a stored database hash."""
    try:
        return ph.verify(hashed_password, plain_password)
    except Exception:
        return False