import os
API_SECRET = os.getenv("API_SECRET", "shamil")

def validate_secret(secret: str) -> bool:
    # Constant-time comparison to prevent timing attacks
    from hmac import compare_digest
    return compare_digest(secret, API_SECRET)
