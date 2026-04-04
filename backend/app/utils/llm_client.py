import os
import json
import hashlib
from functools import lru_cache
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage

# Simple in-memory cache for LLM responses
_response_cache: dict[str, str] = {}



def _get_llm() -> ChatOllama:
    """Get configured LLM instance."""
    return ChatOllama(
        model=os.getenv("LLM_MODEL", "minimax-m2.5:cloud"),
        temperature=0.3,
        #api_key=os.getenv("GROQ_API_KEY", "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"),
        max_tokens=4000,
    )


def _cache_key(system: str, user: str) -> str:
    """Generate a cache key from prompts."""
    content = f"{system}||{user}"
    return hashlib.md5(content.encode()).hexdigest()


def call_llm(system_prompt: str, user_prompt: str, use_cache: bool = True) -> str:
    """
    Call the LLM with system and user prompts.
    Returns the raw string response.
    Caches responses by default to avoid redundant API calls.
    """
    key = _cache_key(system_prompt, user_prompt)

    if use_cache and key in _response_cache:
        return _response_cache[key]

    llm = _get_llm()
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]
    response = llm.invoke(messages)
    result = response.content

    if use_cache:
        _response_cache[key] = result

    return result


def call_llm_json(system_prompt: str, user_prompt: str, use_cache: bool = True) -> dict:
    """
    Call LLM and parse the response as JSON.
    Handles common LLM output issues (markdown fences, trailing text).
    """
    raw = call_llm(system_prompt, user_prompt, use_cache)

    # Strip markdown code fences if present
    cleaned = raw.strip()
    if cleaned.startswith("```json"):
        cleaned = cleaned[7:]
    elif cleaned.startswith("```"):
        cleaned = cleaned[3:]
    if cleaned.endswith("```"):
        cleaned = cleaned[:-3]
    cleaned = cleaned.strip()

    try:
        return json.loads(cleaned)
    except json.JSONDecodeError as e:
        raise ValueError(f"LLM returned invalid JSON: {e}\nRaw response:\n{raw[:500]}")
