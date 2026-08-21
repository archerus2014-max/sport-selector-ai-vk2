import os
from dotenv import load_dotenv


load_dotenv()


VK_TOKEN = os.getenv(
    "VK_TOKEN"
)


VK_GROUP_ID = int(
    os.getenv(
        "VK_GROUP_ID",
        0
    )
)


CALLBACK_SECRET = os.getenv(
    "CALLBACK_SECRET"
)

