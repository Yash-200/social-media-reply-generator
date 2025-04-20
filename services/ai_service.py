from typing import Dict, List
import json
from groq import Groq
from config import settings

class AIService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        
    def _get_platform_context(self, platform: str) -> Dict:
        platform_contexts = {
            "twitter": {
                "max_length": 280,
                "style": "casual, concise, often using hashtags",
                "tone": "conversational and engaging"
            },
            "linkedin": {
                "max_length": 1300,
                "style": "professional but personable",
                "tone": "constructive and insightful"
            },
            "instagram": {
                "max_length": 2200,
                "style": "visual-focused, emoji-friendly",
                "tone": "positive and expressive"
            }
        }
        return platform_contexts.get(platform.lower(), {})

    def generate_reply(self, platform: str, post_text: str) -> str:
        platform_context = self._get_platform_context(platform)
        
        analysis_prompt = {
            "role": "system",
            "content": json.dumps({
                "task": "Analyze social media post",
                "steps": [
                    "1. Identify post tone (formal, casual, excited, etc.)",
                    "2. Extract key topics and sentiment",
                    "3. Note any hashtags, mentions, or special formatting",
                    "4. Consider platform-specific context"
                ]
            })
        }
        
        generation_prompt = {
            "role": "system",
            "content": f"""You are crafting a reply on {platform}. Consider:
            - Platform style: {platform_context['style']}
            - Tone: {platform_context['tone']}
            - Max length: {platform_context['max_length']} characters
            - Must feel authentic and personal
            - Avoid generic statements
            - Match the original post's energy level
            """
        }

        try:
            analysis = self.client.chat.completions.create(
                messages=[
                    analysis_prompt,
                    {"role": "user", "content": post_text}
                ],
                model=settings.MODEL_NAME,
                temperature=0.7
            )
            
            response = self.client.chat.completions.create(
                messages=[
                    generation_prompt,
                    {"role": "user", "content": f"Post: {post_text}\nAnalysis: {analysis.choices[0].message.content}"}
                ],
                model=settings.MODEL_NAME,
                temperature=0.8
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise Exception(f"Error generating reply: {str(e)}") 