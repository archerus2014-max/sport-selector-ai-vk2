import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass(frozen=True)
class Settings:
    VK_TOKEN: str = os.getenv("VK_TOKEN", "")
    VK_CONFIRMATION_CODE: str = os.getenv("VK_CONFIRMATION_CODE", "")
    VK_SECRET: str = os.getenv("VK_SECRET", "")
    VK_API_VERSION: str = os.getenv("VK_API_VERSION", "5.199")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-5.6")

settings = Settings()
