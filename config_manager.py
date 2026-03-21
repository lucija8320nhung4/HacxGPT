"""
Local configuration manager for API keys and provider settings.
All data is stored on your machine only - nothing is sent to external servers.
"""
import json
import os

CONFIG_DIR = os.path.join(os.path.expanduser("~"), ".hacxgpt_cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")

PROVIDERS = {
    "openrouter": {
        "name": "OpenRouter",
        "url": "https://openrouter.ai/keys",
        "models": ["mimo-v2-flash", "devstral-2512", "glm-4.5-air", "kimi-k2", "deepseek-r1t-chimera", "llama-3.3-70b"],
    },
    "groq": {
        "name": "Groq",
        "url": "https://console.groq.com/keys",
        "models": ["kimi-k2-instruct-0905", "qwen3-32b"],
    },
    "hacxgpt": {
        "name": "HacxGPT API",
        "url": "https://hacxgpt.com",
        "models": ["hacxgpt-lightning"],
    },
    "minimax": {
        "name": "MiniMax",
        "url": "https://platform.minimaxi.com",
        "models": ["MiniMax-M2.5", "MiniMax-M2.5-highspeed"],
    },
}


def get_config():
    """Load configuration from local file."""
    if not os.path.exists(CONFIG_FILE):
        return {
            "provider": "openrouter",
            "model": "mimo-v2-flash",
            "api_key": "",
        }
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError):
        return {
            "provider": "openrouter",
            "model": "mimo-v2-flash",
            "api_key": "",
        }


def save_config(provider: str, model: str, api_key: str):
    """Save configuration locally. API key is stored only on your machine."""
    os.makedirs(CONFIG_DIR, exist_ok=True)
    data = {
        "provider": provider,
        "model": model,
        "api_key": api_key,
    }
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def get_models_for_provider(provider: str):
    """Return list of model IDs for a provider."""
    return PROVIDERS.get(provider, {}).get("models", [])
