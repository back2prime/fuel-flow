def create_cache_key(prefix: str, **kwargs) -> str:
    values = ":".join(str(v) for v in kwargs.values())
    return f"{prefix}:{values}"
