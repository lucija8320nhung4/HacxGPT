"""
Simple AI chat using saved config (OpenRouter / Groq / MiniMax). README: Usage - run and chat.
"""
import json
import sys

from config_manager import get_config, PROVIDERS

def chat_request(messages: list, api_key: str, provider: str, model: str) -> str:
    """Send chat request to provider API. Returns reply text or error message."""
    try:
        import requests
    except ImportError:
        return "[Error] Install dependencies first (option 1). Requires: requests"

    if not api_key or not api_key.strip():
        return "[Error] Set your API key in Settings first."

    if provider == "openrouter":
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://hacxgpt.com",
        }
        payload = {"model": model, "messages": messages}
    elif provider == "groq":
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages}
    elif provider == "minimax":
        url = "https://api.minimax.io/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key.strip()}",
            "Content-Type": "application/json",
        }
        payload = {"model": model, "messages": messages}
    elif provider == "hacxgpt":
        return "[Info] HacxGPT API: visit hacxgpt.com for endpoint and usage."
    else:
        return f"[Error] Unknown provider: {provider}"

    if provider in ("openrouter", "groq", "minimax"):
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=60)
            r.raise_for_status()
            data = r.json()
            choice = data.get("choices", [{}])[0]
            return choice.get("message", {}).get("content", "").strip() or "[Empty response]"
        except requests.exceptions.RequestException as e:
            return f"[API Error] {str(e)}"
        except (KeyError, IndexError, json.JSONDecodeError) as e:
            return f"[Parse Error] {str(e)}"
    return ""
