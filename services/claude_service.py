import os
import anthropic
from datetime import datetime, timedelta
from functools import lru_cache
import json

class ClaudeService:
    def __init__(self):
        self.client = anthropic.Client(api_key=os.environ.get('ANTHROPIC_API_KEY'))
        self.cache_timeout = timedelta(hours=24)

    @lru_cache(maxsize=100)
    def generate_study_guide(self, input_text, format_type):
        cache_key = f"{input_text}:{format_type}"
        
        prompts = {
            'flashcards': "Create a set of flashcards from this text, with clear questions and answers:",
            'quiz': "Generate a multiple choice quiz from this content with 5 questions:",
            'summary': "Create a concise, ADHD-friendly summary with bullet points and key concepts:"
        }
        
        prompt = f"{prompts.get(format_type, prompts['summary'])}\n\n{input_text}"
        
        try:
            response = self.client.messages.create(
                model="claude-instant-1.2",
                max_tokens=1500,
                temperature=0.7,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content
        except Exception as e:
            return f"Error generating study guide: {str(e)}"

    def clear_old_cache_entries(self):
        # Clear cache entries older than cache_timeout
        current_time = datetime.utcnow()
        self.generate_study_guide.cache_info()
