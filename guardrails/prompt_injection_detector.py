"""
Prompt Injection Detector Guardrail
Detects common prompt injection patterns and jailbreak attempts.

Category: security
Input Type: request
"""

def apply_guardrail(inputs, request_data, input_type):
    """Detect prompt injection attempts
    
    Looks for common patterns used in:
    - Instruction override attempts
    - Jailbreak prompts
    - Role manipulation
    - DAN mode triggers
    
    Returns:
        block() if injection detected, allow() otherwise
    """
    text = ' '.join(inputs.get('texts', [])).lower()
    
    # Common injection patterns
    injection_patterns = [
        r'ignore (all |previous |above )?instructions',
        r'disregard (all |previous |above )?instructions',
        r'forget (all |previous |above )?instructions',
        r'you are now',
        r'new persona',
        r'act as if',
        r'pretend (that )?you',
        r'jailbreak',
        r'dan mode',
        r'developer mode'
    ]
    
    for pattern in injection_patterns:
        if regex_match(pattern, text):
            return block(f'Potential prompt injection detected: {pattern}')
    
    return allow()
