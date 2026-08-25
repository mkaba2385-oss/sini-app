import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://kaba:123654@localhost:5432/sini",
)
