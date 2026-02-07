"""
API Key Detector Guardrail
Detects and blocks accidental API key exposure in prompts.

Category: security
Input Type: request
"""

def apply_guardrail(inputs, request_data, input_type):
    """Detect API keys and secrets in input
    
    Detects patterns for:
    - OpenAI API keys (sk-...)
    - Anthropic API keys (sk-ant-...)
    - AWS Access Keys (AKIA...)
    - GitHub tokens (ghp_/ghs_...)
    - Stripe keys (sk_live_...)
    - Generic API key patterns
    
    Returns:
        block() if API key detected, allow() otherwise
    """
    text = ' '.join(inputs.get('texts', []))
    
    # Common API key patterns
    patterns = {
        'OpenAI': r'sk-[a-zA-Z0-9]{48}',
        'Anthropic': r'sk-ant-[a-zA-Z0-9-]{95}',
        'AWS': r'AKIA[0-9A-Z]{16}',
        'GitHub': r'gh[ps]_[a-zA-Z0-9]{36}',
        'Stripe': r'sk_live_[a-zA-Z0-9]{24}',
        'Generic': r'[a-zA-Z0-9_-]*[aA][pP][iI][_-]?[kK][eE][yY][a-zA-Z0-9_-]*=[a-zA-Z0-9_-]{20,}'
    }
    
    for provider, pattern in patterns.items():
        if regex_match(pattern, text):
            return block(f'Potential {provider} API key detected - do not share secrets with LLMs')
    
    return allow()
