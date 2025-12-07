from passlib.context import CryptContext


password_context = CryptContext(
    schemes=['bcrypt']
)


def get_password_hash(password: str) -> str:
    hash_string = password_context.hash(password)
    return hash_string


def verify_password(password: str, hash_string: str) -> bool:
    return password_context.verify(password, hash_string) 
    