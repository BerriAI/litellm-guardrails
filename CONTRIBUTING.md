# Contributing to LiteLLM Guardrails Marketplace

Thank you for your interest in contributing! This guide will help you add new guardrails to the marketplace.

## Contribution Guidelines

### 1. Guardrail Quality Standards

- **Tested**: Your guardrail should work correctly with LiteLLM
- **Documented**: Clear description and example use cases
- **Safe**: No malicious code or security vulnerabilities
- **Useful**: Solves a real problem for LLM users

### 2. Sandbox Restrictions

Custom code guardrails run in a restricted sandbox. You **cannot**:

- Import external modules
- Access the filesystem
- Use `exec()` or `eval()`
- Make arbitrary network requests

You **can** use the built-in primitives:
- `regex_match`, `regex_replace`, `regex_find_all`
- `json_parse`, `json_stringify`, `json_schema_valid`
- `extract_urls`, `detect_code`
- `http_get`, `http_post` (sandbox-approved URLs only)

### 3. How to Contribute

#### Option A: Quick Add (JSON only)

1. Fork this repository
2. Edit `guardrails.json`
3. Add your guardrail with all required fields
4. Submit a Pull Request

#### Option B: Full Contribution (recommended)

1. Fork this repository
2. Add entry to `guardrails.json`
3. Create `guardrails/your_guardrail_id.py` with the full code and comments
4. Update `README.md` table if adding a notable guardrail
5. Submit a Pull Request

### 4. JSON Schema

```json
{
  "guardrail_id": {
    "name": "Human Readable Name",
    "description": "One-line description of what it does",
    "category": "security|validation|moderation|rate-limiting|content|formatting",
    "tags": ["searchable", "tags"],
    "author": "Your Name",
    "version": "1.0.0",
    "input_type": "request|response|both",
    "code": "def apply_guardrail(inputs, request_data, input_type):\n    return allow()"
  }
}
```

### 5. Categories

| Category | Icon | Use For |
|----------|------|---------|
| security | 🔒 | PII, secrets, injection attacks |
| validation | ✅ | Schema validation, format checks |
| moderation | 🛡️ | Content filtering, toxicity |
| rate-limiting | ⏱️ | Quotas, usage limits |
| content | 📝 | Code detection, content analysis |
| formatting | ✨ | Output cleaning, formatting |

### 6. Testing Your Guardrail

Before submitting, test your guardrail locally:

```python
# Test helper
def test_guardrail():
    inputs = {"texts": ["Test input"], "images": [], "tool_calls": []}
    request_data = {"model": "gpt-4", "messages": [], "metadata": {}}
    
    result = apply_guardrail(inputs, request_data, "request")
    print(result)
```

### 7. Pull Request Checklist

- [ ] Guardrail added to `guardrails.json`
- [ ] All required fields present (name, description, category, tags, author, version, input_type, code)
- [ ] Code is properly escaped in JSON (newlines as `\n`)
- [ ] Tested locally
- [ ] No external imports or unsafe operations
- [ ] Description is clear and concise

## Questions?

- Open an issue for questions
- Join the [LiteLLM Discord](https://discord.gg/litellm)
- Check the [LiteLLM docs](https://docs.litellm.ai)

Thank you for making LiteLLM better! 🚀
