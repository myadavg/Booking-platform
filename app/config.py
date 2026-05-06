import os



class Settings:
    DATABASE_URL = os.getenv("DATABASE_URL")
    APP_ENV = os.getenv("APP_ENV", "dev")
    APP_NAME = os.getenv("APP_NAME", "Booking Platform")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")


settings = Settings()
