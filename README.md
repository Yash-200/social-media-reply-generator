# Social Media Reply Generator

A FastAPI-based service that generates human-like replies to social media posts using AI. The system uses Groq's LLM to create contextually appropriate responses for different social media platforms.

## Features

- Platform-specific reply generation for Twitter, LinkedIn, and Instagram
- Multi-step AI processing for more natural responses
- Database storage of all post-reply pairs
- RESTful API with FastAPI
- Docker support
- Comprehensive error handling
- Input validation using Pydantic

## Tech Stack

- Python 3.9+
- FastAPI
- SQLAlchemy (SQLite)
- Groq AI
- Pydantic
- Docker

## Installation

### Local Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd social-media-reply-generator
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Create a `.env` file in the project root:
```env
GROQ_API_KEY=your-groq-api-key
DATABASE_URL=sqlite:///./social_replies.db
MODEL_NAME=llama3-8b-8192
```

5. Run the application:
```bash
uvicorn test:app --reload
```

### Docker Setup

1. Build the image:
```bash
docker build -t social-media-reply-generator .
```

2. Run the container with environment variables:
```bash
docker run -p 8000:8000 \
  -e GROQ_API_KEY="your_api_key_here" \
  social-media-reply-generator
```

Alternatively, you can create a `.env` file and use it:
```bash
docker run -p 8000:8000 \
  --env-file .env \
  social-media-reply-generator
```

Example `.env` file:
```env
GROQ_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./social_replies.db
MODEL_NAME=llama3-8b-8192
```

**Important**: Never commit your `.env` file to version control. Add it to `.gitignore`:

## API Usage

### Generate Reply

```