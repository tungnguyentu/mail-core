from environs import Env

env = Env()
env.read_env()


class Settings:
    DEFAULT_INTERVAL = env.int("DEFAULT_INTERVAL", default=600)
    SQLALCHEMY_DATABASE_URI = env.str(
        "SQLALCHEMY_DATABASE_URI", default="sqlite:///:memory:"
    )
