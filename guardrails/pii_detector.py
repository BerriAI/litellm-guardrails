"""
PII Detector Guardrail
Detects and blocks personally identifiable information like SSNs, credit cards, and phone numbers.

Category: security
Input Type: request
"""

def apply_guardrail(inputs, request_data, input_type):
    """Block requests containing PII patterns
    
    Detects:
    - Social Security Numbers (XXX-XX-XXXX format)
    - Credit card numbers (16 digits with optional separators)
    - Phone numbers (when more than 2 are present)
    
    Returns:
        block() if PII detected, allow() otherwise
    """
    text = ' '.join(inputs.get('texts', []))
    
    # SSN pattern
    ssn_matches = regex_find_all(r'\b\d{3}-\d{2}-\d{4}\b', text)
    if ssn_matches:
        return block('SSN detected in input')
    
    # Credit card pattern (basic)
    cc_matches = regex_find_all(r'\b\d{4}[- ]?\d{4}[- ]?\d{4}[- ]?\d{4}\b', text)
    if cc_matches:
        return block('Credit card number detected in input')
    
    # Phone number pattern
    phone_matches = regex_find_all(r'\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b', text)
    if len(phone_matches) > 2:
        return block('Multiple phone numbers detected')
    
    return allow()
