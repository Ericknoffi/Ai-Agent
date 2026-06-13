import re


_PATTERNS: dict[str, re.Pattern] = {
    "email": re.compile(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    ),
    "phone": re.compile(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b"
    ),
    "aadhaar": re.compile(
        r"\b\d{4}\s\d{4}\s\d{4}\b"          
    ),
    "pan": re.compile(
        r"\b[A-Z]{5}[0-9]{4}[A-Z]\b"
    ),
    "passport": re.compile(
        r"\b[A-Z][0-9]{7}\b"
    ),
    "driving_license": re.compile(
        r"\b[A-Z]{2}[0-9]{2}[0-9]{11,13}\b"
    ),
   
    "ifsc": re.compile(
        r"\b[A-Z]{4}0[A-Z0-9]{6}\b"
    ),
  
    "card_number": re.compile(
        r"\b(?:4[0-9]{12}(?:[0-9]{3})?|5[1-5][0-9]{14}|3[47][0-9]{13}|6(?:011|5[0-9]{2})[0-9]{12})\b"
    ),
 
    "upi": re.compile(
        r"\b[a-zA-Z0-9._-]+@(?:okaxis|oksbi|okicici|okhdfcbank|paytm|ybl|ibl|axl|upi)\b"
    ),
    "github_token": re.compile(
        r"\bgh[pousr]_[A-Za-z0-9_-]+\b"
    ),
    "openai_key": re.compile(
        r"\bsk-[A-Za-z0-9_-]{20,}\b"       
    ),
    "jwt": re.compile(
        r"\beyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+\b"
    ),
    "ip_v6": re.compile(
        r"\b(?:[0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}\b"
    ),
   
    "ip_v4": re.compile(
        r"\b(?:(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\.){3}"
        r"(?:25[0-5]|2[0-4]\d|1\d{2}|[1-9]\d|\d)\b"
    ),
}


def redact_pii(text: str) -> str:
    if not text:
        return text
    for pattern in _PATTERNS.values():
        text = pattern.sub("[REDACTED]", text)
    return text
