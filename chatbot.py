import requests
from config import GROQ_API_KEY, MODEL, SYSTEM_PROMPT

API_URL = "https://api.groq.com/openai/v1/chat/completions"

def get_response(conversation_history: list) -> str:
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + conversation_history

    payload = {
        "model": MODEL,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Connection error. Please check your internet and try again."
    except Exception as e:
        return f"Something went wrong: {str(e)}"


def build_history(messages: list) -> list:
    """Convert Streamlit session messages to Groq format."""
    return [
        {"role": m["role"], "content": m["content"]}
        for m in messages
    ]
