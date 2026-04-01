import os
from dotenv import load_dotenv

load_dotenv()


class Config:

    API_URL = os.getenv("BASE_API_URL", "http://localhost:9000")
    ADMIN_URL = os.getenv("BASE_ADMIN_URL", "http://localhost:9000/app")
    STOREFRONT_URL = os.getenv("BASE_STOREFRONT_URL", "http://localhost:8000")

    ADMIN_EMAIL = os.getenv("ADMIN_EMAIL", "admin@medusa-test.com")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "supersecret")

    UI_TIMEOUT = int(os.getenv("UI_TIMEOUT", "5000"))
    API_TIMEOUT = int(os.getenv("API_TIMEOUT", 10000))
    HEADLESS_MODE = os.getenv("HEADLESS_MODE", "False").lower() == "true"
