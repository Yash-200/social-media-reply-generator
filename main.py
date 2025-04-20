from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from groq import Groq
from sqlalchemy import create_engine, Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from fastapi import Depends
from sqlalchemy.orm import Session
from models import ReplyRequest, ReplyResponse, ErrorResponse, Platform
from services.ai_service import AIService
from config import settings

app = FastAPI()

client = Groq(
    api_key=settings.GROQ_API_KEY,
)

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./social_replies.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class PostReply(Base):
    __tablename__ = "post_replies"
    
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String)
    post_text = Column(Text)
    reply = Column(Text)
    created_at = Column(String)

Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ChatRequest(BaseModel):
    message: str

ai_service = AIService()

@app.get("/")
async def root():
    return {"message": "Welcome to the Groq Chat Completion API"}

@app.post("/chat")
async def chat_completion(request: ChatRequest):
    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": request.message,
                }
            ],
            model="llama3-8b-8192",
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/reply", response_model=ReplyResponse, responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}})
async def generate_reply(request: ReplyRequest, db: Session = Depends(get_db)):
    """
    Generate a human-like reply to a social media post.
    
    Args:
        request (ReplyRequest): Platform and post text information
        
    Returns:
        ReplyResponse: Generated reply with metadata
        
    Raises:
        HTTPException: If platform is unsupported or generation fails
    """
    try:
        reply = ai_service.generate_reply(request.platform, request.post_text)
        
        # Store in database
        db_reply = PostReply(
            platform=request.platform,
            post_text=request.post_text,
            reply=reply,
            created_at=datetime.now().isoformat()
        )
        db.add(db_reply)
        db.commit()

        return ReplyResponse(
            platform=request.platform,
            post_text=request.post_text,
            reply=reply,
            created_at=datetime.now()
        )
        
    except Exception as e:
        # Add more detailed error logging
        import traceback
        error_detail = f"Error: {str(e)}\nTraceback: {traceback.format_exc()}"
        print(error_detail)  # This will show in Docker logs
        raise HTTPException(status_code=500, detail=error_detail)

@app.get("/replies")
async def get_replies(
    platform: str = None,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    query = db.query(PostReply)
    if platform:
        query = query.filter(PostReply.platform == platform)
    replies = query.order_by(PostReply.id.desc()).limit(limit).all()
    return [{"platform": r.platform, "post_text": r.post_text, "reply": r.reply, "created_at": r.created_at} for r in replies]
