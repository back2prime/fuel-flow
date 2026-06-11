import re


def create_cache_key(prefix: str, **kwargs) -> str:
    values = ":".join(str(v) for v in kwargs.values())
    return f"{prefix}:{values}"


def validate_password(password: str) -> list[str]:
    errors = []
    if len(password) < 12:
        errors.append("Password must be at least 12 characters long")
    if not re.search(r"[A-Z]", password):
        errors.append("Password must contain an uppercase letter")
    if not re.search(r"[a-z]", password):
        errors.append("Password must contain a lowercase letter")
    if not re.search(r"\d", password):
        errors.append("Password must contain a digit")
    if not re.search(r"[^\w\s]", password):
        errors.append("Password must contain a special character")
    return errors


def password_strength_validator(v: str) -> str:
    errors = validate_password(v)
    if errors:
        raise ValueError(", ".join(errors))
    return v
