# Agent Router API - Before/After Examples

## Problem
Calling Agent Router API directly returns 401 "unauthorized client detected"

## Solution
Add 10 required headers that mimic the Roo Code client

---

## Quick Start

1. Install: `pip install -r requirements.txt`
2. Create `.env` file:
   ```
   API_KEY=your-api-key
   ```
3. Run the scripts

---

## Before (FAILS - 401)

```bash
python before.py "Hello"
```

```python
# before.py
response = httpx.post(
    "https://agentrouter.org/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    },
    json={
        "model": "deepseek-v3.2",
        "messages": [{"role": "user", "content": prompt}]
    }
)

# Response: 401 - {"error": {"message": "unauthorized client detected"}}
```

---

## After (WORKS - 200)

```bash
python after.py "Hello"
```

```python
# after.py
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
        "messages": [{"role": "user", "content": prompt}]
    }
)

# Response: 200 - {"choices": [{"message": {"content": "..."}}]}
```

---

## Disclaimer

⚠️ **For testing/development only.** May violate API terms of use. Contact Agent Router for official access.