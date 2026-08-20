import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://sini:sini@localhost:5432/sini",
)
