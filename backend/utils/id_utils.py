import hashlib

def generate_id(text: str, prefix: str) -> str:
    h = hashlib.md5(text.encode()).hexdigest()[:12]
    return f"{prefix}_{h}"