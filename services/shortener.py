import string
import secrets

# 62 possible characters (26 lowercase + 26 uppercase + 10 digits)
BASE62 = string.ascii_letters + string.digits


def shorten_B62(length: int = 6) -> str:
    return "".join(secrets.choice(BASE62) for _ in range(length))
