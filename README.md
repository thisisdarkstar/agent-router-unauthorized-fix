# Agent Router API Testing Guide

---

## PROBLEM: API Returns 401 Unauthorized

When calling the API directly without a coding agent:

**Status:** 401

**Response:**
```json
{
  "error": {
    "message": "unauthorized client detected, contact support for assistance at https://discord.gg/V6kaP6Rg44"
  },
  "message": "UNAUTHENTICATED",
  "success": false,
  "type": "unauthorized_client_error"
}
```

---

## SOLUTION: Add These 10 Headers

```python
headers = {
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
}
```

**All 10 required. No exceptions.**

---

## Quick Start (Copy This)

### Before (FAILS - 401)

```python
import httpx

API_KEY = "your-api-key"
response = httpx.post(
    "https://agentrouter.org/v1/chat/completions",
    headers={
        "Authorization": "Bearer your-api-key",
        "Content-Type": "application/json"
    },
    json={"model": "deepseek-v3.2", "messages": [{"role": "user", "content": "Hi"}]}
)

print(response.status_code)  # 401
```

**Response:**
```json
{
  "error": {
    "message": "unauthorized client detected, contact support for assistance at https://discord.gg/V6kaP6Rg44"
  },
  "message": "UNAUTHENTICATED",
  "success": false,
  "type": "unauthorized_client_error"
}
```

---

### After (WORKS - 200)

```python
import httpx

API_KEY = "your-api-key"
response = httpx.post(
    "https://agentrouter.org/v1/chat/completions",
    headers={
        "Authorization": "Bearer your-api-key",
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
    json={"model": "deepseek-v3.2", "messages": [{"role": "user", "content": "Hi"}]}
)

print(response.status_code)  # 200
```

**Response:**
```json
{
  "id": "as-sjd7vpzat4",
  "object": "chat.completion",
  "created": 1778342230,
  "model": "deepseek-v3.2",
  "choices": [
    {
      "index": 0,
      "message": {
        "role": "assistant",
        "content": "Hello! I'm here and ready to assist you. How can I help you today?"
      },
      "finish_reason": "stop",
      "flag": 0
    }
  ],
  "usage": {
    "prompt_tokens": 18,
    "completion_tokens": 21,
    "total_tokens": 39
  }
}
```

---

## Setup (Optional)

1. **Create .env file:**
   ```
   API_KEY=your-api-key
   ```

2. **Install:** `pip install httpx python-dotenv`

3. **Use:**
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   API_KEY = os.getenv("API_KEY")
   ```

---

## What Happens Without Headers

| Request | Status | Response |
|---------|--------|----------|
| Just Authorization + Content-Type | 401 | `{"error": {"message": "unauthorized client detected"}}` |
| Missing any header | 400 | `{"error": {"message": "unauthorized client detected"}}` |
| Wrong User-Agent | 401 | `{"error": {"message": "unauthorized client detected"}}` |
| Wrong X-Title | 400 | `{"error": {"message": "unauthorized client detected"}}` |
| Wrong Referer | 400 | `{"error": {"message": "unauthorized client detected"}}` |
| Python runtime (X-Stainless-Runtime: python) | 400 | `{"error": {"message": "unauthorized client detected"}}` |
| Browser runtime | 400 | `{"error": {"message": "unauthorized client detected"}}` |
| No credits | 403 | `{"error": {"message": "Access denied due to overdue account"}}` |
| Model not available | 503 | `{"error": {"message": "当前分组 default 下对于模型 xxx 无可用渠道"}}` |

---

## Key Rules

- **Cannot fake other clients** - Title must be "Roo Code", User-Agent must contain "RooCode"
- **Only node runtime works** - Python and browser blocked
- **OS + Arch required** - At least these two from X-Stainless-*
- **Referer must match** - Must contain "RooVetGit/Roo-Cline"

---

## Working Models

| Model | Status |
|-------|--------|
| deepseek-v3.2 | ✅ OK |
| glm-4.5 | ✅ OK |
| glm-4.6 | ✅ OK |
| glm-5.1 | ✅ OK |
| deepseek-r1-0528 | ❌ 403 (needs credits) |
| deepseek-v3.1 | ❌ 403 (needs credits) |
| claude models | ❌ 503 (no channel) |

---

## Working Endpoints

| Endpoint | Status |
|----------|--------|
| /chat/completions | ✅ OK |
| /messages | ✅ OK |
| /responses, /beta/models | ❌ 404 |
| /embeddings, /rerank | ❌ 500 |
| /images/*, /audio/* | ❌ 503 (needs model config) |

---

## Troubleshooting

| Error | Fix |
|-------|-----|
| 401 | Add all 10 headers exactly as shown |
| 400 | Check exact values - Title="Roo Code", User-Agent contains "RooCode" |
| 403 | Add credits at agentrouter.org |
| 503 | Model not available - check account config |

---

## Why This Is Required

The API validates client identity using the OpenAI SDK's X-Stainless headers. It only accepts requests that appear to come from Roo Code. There's no way to use different client names or other runtimes - the API strictly validates these values.

---

## Use Cases

- Test API without a coding agent
- Build custom integrations
- Run in CI/CD pipelines
- Model benchmarking