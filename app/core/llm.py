import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# LLM Configuration - supports multiple providers
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "mock")  # Options: ollama, openai, mock

def generate_llama_answer(prompt: str):
    if LLM_PROVIDER == "ollama":
        return _generate_ollama_answer(prompt)
    elif LLM_PROVIDER == "openai":
        return _generate_openai_answer(prompt)
    else:  # mock
        return _generate_mock_answer(prompt)

def _generate_ollama_answer(prompt: str):
    """Generate answer using local Ollama service"""
    try:
        payload = {"model": "gemma:2b", "prompt": prompt, "stream": False}
        response = requests.post("http://localhost:11434/api/generate", json=payload)
        response.raise_for_status()
        data = response.json()
        return data["response"]
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama service not available. Please start Ollama: 'ollama serve' and pull model: 'ollama pull gemma:2b'. Error: {e}")

def _generate_openai_answer(prompt: str):
    """Generate answer using OpenAI API"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise Exception("OPENAI_API_KEY environment variable not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 500
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"]

def _generate_mock_answer(prompt: str):
    """Generate mock answer for testing"""
    return f"This is a mock response for testing. Your question was: '{prompt[:100]}...'. Please configure a real LLM provider (Ollama or OpenAI) for production use."
