import httpx
import sys
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
prompt = sys.argv[1] if len(sys.argv) > 1 else "Hello"

response = httpx.post(
    "https://agentrouter.org/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "deepseek-v3.2",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")