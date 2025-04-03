import requests
from django.conf import settings

def call_openrouter_model(prompt, model_name):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",  
        "X-Title": "Turing AI Chat"
    }

    data = {
        "model": model_name,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Xəta: {response.status_code} - {response.text}"
    
def call_model(prompt, model_name):
    supported_models = [
        "deepseek/deepseek-chat",
        "google/gemini-pro"
    ]

    if model_name in supported_models:
        return call_openrouter_model(prompt, model_name)
    return "Bu model dəstəklənmir və ya düzgün yazılmayıb."