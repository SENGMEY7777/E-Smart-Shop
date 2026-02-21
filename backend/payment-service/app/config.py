from pydantic import BaseSettings, SettingsConfigDict, SecretStr, Field

class Settings(BaseSettings):
    # Required variables
    MONGO_URL: str
    BAKONG_MERCHANT_ID: str
    BAKONG_SECRET_KEY: SecretStr
    ORDER_SERVICE_URL: str

    # Use alias so Pydantic reads PORT from env
    port: int = Field(default=4004, alias="PORT")

    # model_config allows the app to ignore other system variables
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"  # prevents crash from unexpected env vars
    )

settings = Settings()
