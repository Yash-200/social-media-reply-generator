# API Documentation

## Base URL
`http://localhost:8000`

## Endpoints

### 1. Generate Reply
Generate a human-like reply to a social media post.

**Endpoint:** `/reply`
**Method:** POST

**Request Body:**
```json
{
    "platform": string,    // "twitter", "linkedin", or "instagram"
    "post_text": string   // The social media post text
}
```

**Response:**
```json
{
    "platform": string,
    "post_text": string,
    "reply": string,
    "created_at": string
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/reply" \
     -H "Content-Type: application/json" \
     -d '{
           "platform": "twitter",
           "post_text": "Excited to share my new project!"
         }'
```

### 2. Get Previous Replies
Retrieve previously generated replies.

**Endpoint:** `/replies`
**Method:** GET

**Query Parameters:**
- `platform` (optional): Filter by platform
- `limit` (optional): Maximum number of replies to return (default: 10)

**Response:**
```json
[
    {
        "platform": string,
        "post_text": string,
        "reply": string,
        "created_at": string
    }
]
```

**Example:**
```bash
curl "http://localhost:8000/replies?platform=twitter&limit=5"
```

### 3. Root Endpoint
Get API status.

**Endpoint:** `/`
**Method:** GET

**Response:**
```json
{
    "message": "Welcome to the Groq Chat Completion API"
}
```

## Error Responses

### 400 Bad Request
Returned when:
- Invalid platform specified
- Invalid input format

```json
{
    "detail": "Error message describing the issue"
}
```

### 500 Internal Server Error
Returned when:
- AI generation fails
- Database errors occur

```json
{
    "detail": "Error message describing the issue"
}
```

## Platform-Specific Considerations

### Twitter
- Maximum reply length: 280 characters
- Style: Casual, concise, often using hashtags
- Tone: Conversational and engaging

### LinkedIn
- Maximum reply length: 1300 characters
- Style: Professional but personable
- Tone: Constructive and insightful

### Instagram
- Maximum reply length: 2200 characters
- Style: Visual-focused, emoji-friendly
- Tone: Positive and expressive

## Rate Limiting
[Add rate limiting information if implemented]

## Authentication
[Add authentication information if implemented]

## Best Practices
1. Always validate input before sending
2. Handle errors gracefully in your client application
3. Consider implementing retry logic for failed requests
4. Monitor response times and implement appropriate timeouts 