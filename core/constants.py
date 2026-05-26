from pathlib import Path

BACKEND_DIR = Path(__file__).parent.parent
HTTP_URL = "https://creativecommons.tankerkoenig.de/json/"
REDIS_URL = "redis://localhost:6379/0"
JWT_EXPIRE_SECONDS = 1800