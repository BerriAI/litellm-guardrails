# LiteLLM Guardrails Marketplace

A community collection of custom code guardrails for [LiteLLM](https://github.com/BerriAI/litellm). Browse, copy, and deploy guardrails to protect your LLM applications.

🌐 **Live Site:** [models.litellm.ai/guardrails](https://models.litellm.ai/guardrails)

## What are Custom Code Guardrails?

Custom code guardrails are Python functions that run before (pre-call) or after (post-call) your LLM requests. They can:

- **Block** harmful or policy-violating content
- **Modify** inputs/outputs (redact PII, format responses)
- **Allow** requests to proceed normally

Learn more: [LiteLLM Custom Code Guardrails Documentation](https://docs.litellm.ai/docs/proxy/guardrails/custom_code_guardrail)

## Available Guardrails

| Name | Category | Type | Description |
|------|----------|------|-------------|
| `pii_detector` | 🔒 Security | Request | Detects and blocks PII (SSNs, credit cards, phones) |
| `pii_redactor` | 🔒 Security | Request | Redacts PII with `[REDACTED]` markers |
| `prompt_injection_detector` | 🔒 Security | Request | Detects jailbreak and injection attempts |
| `api_key_detector` | 🔒 Security | Request | Prevents accidental API key exposure |
| `url_validator` | 🔒 Security | Request | Blocks suspicious URLs and phishing domains |
| `json_schema_validator` | ✅ Validation | Response | Validates responses against JSON schemas |
| `word_count_limit` | ✅ Validation | Both | Enforces word count limits |
| `language_detector` | ✅ Validation | Request | Detects and restricts content languages |
| `toxic_content_filter` | 🛡️ Moderation | Both | Filters toxic and offensive content |
| `code_detector` | 📝 Content | Response | Detects code and blocks dangerous languages |
| `rate_limit_by_user` | ⏱️ Rate Limiting | Request | Per-user rate limiting template |
| `response_formatter` | ✨ Formatting | Response | Cleans and formats LLM responses |

## Quick Start

### 1. Copy a Guardrail

Find a guardrail you need in `guardrails.json` and copy its code.

### 2. Add to Your LiteLLM Config

```yaml
# config.yaml
litellm_settings:
  guardrails:
    - guardrail_name: "pii_detector"
      litellm_params:
        guardrail: custom_code.pii_detector
        mode: "pre_call"  # or "post_call" for response guardrails
```

### 3. Save Your Guardrail Code

Save the guardrail function in a file referenced by your config, or add it directly via the LiteLLM UI.

## Contributing a Guardrail

We welcome contributions! Here's how to add a new guardrail:

### 1. Fork this repository

### 2. Add your guardrail to `guardrails.json`

```json
{
  "your_guardrail_id": {
    "name": "Your Guardrail Name",
    "description": "Brief description of what it does",
    "category": "security|validation|moderation|rate-limiting|content|formatting",
    "tags": ["relevant", "tags", "for", "search"],
    "author": "Your Name or GitHub handle",
    "version": "1.0.0",
    "input_type": "request|response|both",
    "code": "def apply_guardrail(inputs, request_data, input_type):\n    # Your code here\n    return allow()"
  }
}
```

### 3. Create a standalone file in `guardrails/`

```python
# guardrails/your_guardrail_id.py
def apply_guardrail(inputs, request_data, input_type):
    """
    Description of your guardrail.
    
    Args:
        inputs: Dict with 'texts', 'images', 'tool_calls' lists
        request_data: Full request payload with metadata
        input_type: "request" or "response"
    
    Returns:
        allow(), block(reason), or modify(texts=[], images=[], tool_calls=[])
    """
    # Your implementation
    return allow()
```

### 4. Submit a Pull Request

Include:
- What your guardrail does
- Example use cases
- Any configuration options

## Guardrail Function Signature

```python
def apply_guardrail(inputs, request_data, input_type):
    """
    inputs: {
        "texts": ["message content", ...],
        "images": [...],
        "tool_calls": [...]
    }
    
    request_data: {
        "model": "gpt-4",
        "messages": [...],
        "metadata": {...},
        ...
    }
    
    input_type: "request" | "response"
    
    Returns one of:
        allow()                              # Let it through
        block("reason")                      # Block with message
        modify(texts=[], images=[], ...)     # Transform content
    """
```

## Available Primitives

Custom code guardrails have access to these built-in functions:

| Function | Description |
|----------|-------------|
| `regex_match(pattern, text)` | Check if pattern matches |
| `regex_replace(pattern, replacement, text)` | Replace matches |
| `regex_find_all(pattern, text)` | Find all matches |
| `json_parse(text)` | Parse JSON string |
| `json_stringify(obj)` | Convert to JSON string |
| `json_schema_valid(data, schema)` | Validate against JSON schema |
| `extract_urls(text)` | Extract URLs from text |
| `detect_code(text)` | Detect code blocks |
| `http_get(url)` | Async HTTP GET (sandbox-approved URLs only) |
| `http_post(url, data)` | Async HTTP POST (sandbox-approved URLs only) |

## Development

```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## Deployment

This site is deployed on Vercel. Any push to `main` automatically deploys.

## License

MIT License - see [LICENSE](LICENSE)

---

Built with ❤️ by the [LiteLLM](https://github.com/BerriAI/litellm) team
