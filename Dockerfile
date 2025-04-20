FROM python:3.9-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create database file and set permissions
RUN touch social_replies.db && \
    chmod 666 social_replies.db

# Set environment variables
ENV GROQ_API_KEY="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"
ENV DATABASE_URL="sqlite:///./social_replies.db"
ENV MODEL_NAME="llama3-8b-8192"

# Expose the port
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--log-level", "debug"] 