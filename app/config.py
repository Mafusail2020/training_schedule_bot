from dotenv import load_dotenv
from os import getenv
from pydantic import BaseModel
load_dotenv()


class Config(BaseModel):
    TOKEN: str


config = Config(
    TOKEN=getenv("TOKEN")
)
