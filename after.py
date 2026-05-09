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
        "Content-Type": "application/json",
        "X-Stainless-OS": "Linux",
        "X-Stainless-Arch": "x64",
        "X-Stainless-Lang": "js",
        "X-Stainless-Runtime": "node",
        "X-Stainless-Runtime-Version": "v22.22.1",
        "HTTP-Referer": "https://github.com/RooVetGit/Roo-Cline",
        "X-Title": "Roo Code",
        "User-Agent": "RooCode/3.53.0"
    },
    json={
        "model": "deepseek-v3.2",
        "messages": [{"role": "user", "content": prompt}],
        "stream": False
    }
)

print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")