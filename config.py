from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GROQ_API_KEY: str
    DATABASE_URL: str = "sqlite:///./social_replies.db"
    MODEL_NAME: str = "llama-3.3-70b-versatile"
    
    class Config:
        env_file = ".env"

settings = Settings() 
