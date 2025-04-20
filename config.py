from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str = "sqlite:///./social_replies.db"
    MODEL_NAME: str = "llama3-8b-8192"
    
    class Config:
        env_file = ".env"

settings = Settings() 