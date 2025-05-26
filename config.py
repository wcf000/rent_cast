from pydantic import BaseSettings, Field


class RentCastConfig(BaseSettings):
    """
    Configuration for RentCast API client.
    """
    api_key: str = Field(..., env="RENT_CAST_API_KEY")
    base_url: str = Field("https://api.rentcast.io/v1", env="RENT_CAST_BASE_URL")
    timeout: float = Field(30.0, env="RENT_CAST_TIMEOUT")
    max_retries: int = Field(3, env="RENT_CAST_MAX_RETRIES")

    class Config:
        env_file = ".env"
