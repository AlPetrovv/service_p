import bcrypt

from application.interfaces.security import IPasswordHasher


class BcryptPasswordHasher(IPasswordHasher):
    """Password hashing/verification backed by bcrypt."""

    def hash(self, password: str) -> str:
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, password: str, hashed: str) -> bool:
        try:
            return bcrypt.checkpw(password.encode("utf-8"), hashed.encode("utf-8"))
        except (ValueError, TypeError):
            return False
