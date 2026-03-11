import re

def extract_captions(text):

    captions = []

    patterns = [
        r"(Figure\s\d+[:.\-]\s.*)",
        r"(Fig\.\s\d+[:.\-]\s.*)",
        r"(Table\s\d+[:.\-]\s.*)"
    ]

    for pattern in patterns:

        matches = re.findall(pattern, text, re.IGNORECASE)

        captions.extend(matches)

    captions = [c.strip() for c in captions]

    return captions