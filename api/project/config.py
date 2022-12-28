from decouple import config
from pydantic import BaseModel


class Settings(BaseModel):
    MONGODB_CONNSTRING = config("MONGODB_CONNSTRING")
    DB_NAME = config("DB_NAME", default="admin")
    TESTING = config("TESTING", default=False, cast=bool)


CONFIG = Settings()
