# -*- coding: utf-8 -*-
"""
AI model registry for HacxGPT-CLI.
Centralizes model metadata, capability tags, and context window limits
across all supported providers (OpenRouter, Groq, HacxGPT).
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ModelSpec:
    model_id: str
    display_name: str
    provider: str
    context_window: int
    max_output_tokens: int
    capabilities: List[str] = field(default_factory=list)
    cost_tier: str = "free"
    description: str = ""


MODEL_REGISTRY: Dict[str, ModelSpec] = {
    "mimo-v2-flash": ModelSpec(
        model_id="mimo-v2-flash",
        display_name="Mimo v2 Flash",
        provider="openrouter",
        context_window=32768,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning"],
        cost_tier="free",
        description="Fast general-purpose model with strong coding ability",
    ),
    "devstral-2512": ModelSpec(
        model_id="devstral-2512",
        display_name="Devstral 2512",
        provider="openrouter",
        context_window=131072,
        max_output_tokens=16384,
        capabilities=["chat", "code", "reasoning", "long-context"],
        cost_tier="free",
        description="Mistral-based coding specialist with 128K context",
    ),
    "glm-4.5-air": ModelSpec(
        model_id="glm-4.5-air",
        display_name="GLM 4.5 Air",
        provider="openrouter",
        context_window=32768,
        max_output_tokens=4096,
        capabilities=["chat", "reasoning"],
        cost_tier="free",
        description="Lightweight general chat model",
    ),
    "kimi-k2": ModelSpec(
        model_id="kimi-k2",
        display_name="Kimi K2",
        provider="openrouter",
        context_window=131072,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "long-context"],
        cost_tier="free",
        description="Moonshot AI model with extended context window",
    ),
    "deepseek-r1t-chimera": ModelSpec(
        model_id="deepseek-r1t-chimera",
        display_name="DeepSeek R1T Chimera",
        provider="openrouter",
        context_window=65536,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "math"],
        cost_tier="free",
        description="DeepSeek reasoning model with chain-of-thought",
    ),
    "llama-3.3-70b": ModelSpec(
        model_id="llama-3.3-70b",
        display_name="Llama 3.3 70B",
        provider="openrouter",
        context_window=131072,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "long-context"],
        cost_tier="free",
        description="Meta Llama 3.3 70B instruction-tuned",
    ),
    "kimi-k2-instruct-0905": ModelSpec(
        model_id="kimi-k2-instruct-0905",
        display_name="Kimi K2 Instruct",
        provider="groq",
        context_window=131072,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning"],
        cost_tier="free",
        description="Kimi K2 served via Groq for ultra-low latency",
    ),
    "qwen3-32b": ModelSpec(
        model_id="qwen3-32b",
        display_name="Qwen3 32B",
        provider="groq",
        context_window=32768,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "math"],
        cost_tier="free",
        description="Alibaba Qwen3 32B on Groq inference",
    ),
    "MiniMax-M2.5": ModelSpec(
        model_id="MiniMax-M2.5",
        display_name="MiniMax M2.5",
        provider="minimax",
        context_window=204800,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "long-context"],
        cost_tier="free",
        description="MiniMax M2.5 with 204K context, strong reasoning and coding",
    ),
    "MiniMax-M2.5-highspeed": ModelSpec(
        model_id="MiniMax-M2.5-highspeed",
        display_name="MiniMax M2.5 Highspeed",
        provider="minimax",
        context_window=204800,
        max_output_tokens=8192,
        capabilities=["chat", "code", "reasoning", "long-context"],
        cost_tier="free",
        description="MiniMax M2.5 optimized for speed with 204K context",
    ),
    "hacxgpt-lightning": ModelSpec(
        model_id="hacxgpt-lightning",
        display_name="HacxGPT Lightning",
        provider="hacxgpt",
        context_window=32768,
        max_output_tokens=8192,
        capabilities=["chat", "code", "unrestricted"],
        cost_tier="free",
        description="HacxGPT production model for coding tasks",
    ),
}


def get_models_by_provider(provider: str) -> List[ModelSpec]:
    return [m for m in MODEL_REGISTRY.values() if m.provider == provider]


def get_models_by_capability(capability: str) -> List[ModelSpec]:
    return [m for m in MODEL_REGISTRY.values() if capability in m.capabilities]


def get_model(model_id: str) -> Optional[ModelSpec]:
    return MODEL_REGISTRY.get(model_id)


def get_best_model_for_task(task: str, provider: str = "") -> Optional[ModelSpec]:
    """
    Select the best model for a given task type.
    task: one of 'code', 'chat', 'reasoning', 'math', 'long-context'
    provider: optional filter by provider
    """
    candidates = get_models_by_capability(task)
    if provider:
        candidates = [m for m in candidates if m.provider == provider]
    if not candidates:
        return None
    candidates.sort(key=lambda m: m.context_window, reverse=True)
    return candidates[0]


def format_context_window(tokens: int) -> str:
    if tokens >= 131072:
        return "128K"
    elif tokens >= 65536:
        return "64K"
    elif tokens >= 32768:
        return "32K"
    else:
        return f"{tokens // 1024}K"
