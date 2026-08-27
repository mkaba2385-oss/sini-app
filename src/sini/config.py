import os

from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv(
    "JWT_SECRET_KEY",
    "change-this-secret-key-in-production",
)

JWT_ALGORITHM = "HS256"

ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv(
        "ACCESS_TOKEN_EXPIRE_MINUTES",
        "15",
    )
)

REFRESH_TOKEN_EXPIRE_DAYS = int(
    os.getenv(
        "REFRESH_TOKEN_EXPIRE_DAYS",
        "7",
    )
)

# OpenWeather

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")

OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


# Africa's Talking

AFRICASTALKING_USERNAME = os.getenv("AFRICASTALKING_USERNAME")

AFRICASTALKING_API_KEY = os.getenv("AFRICASTALKING_API_KEY")
