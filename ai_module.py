# ai_module.py
from datetime import datetime
import openai  # Install with: pip install openai

openai.api_key = "your-openai-api-key"

def suggest_priority(task_description):
    """
    Uses OpenAI to suggest a priority for the given task description.
    """
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=f"Suggest a priority for this task: {task_description}",
            max_tokens=10
        )
        return response['choices'][0]['text'].strip()
    except Exception as e:
        print(f"Error in AI suggestion: {e}")
        return "Medium"  # Default priority
