import re


def mask_pii(text: str) -> str:
    text = re.sub(
        r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b",
        "[EMAIL]",
        text,
        flags=re.IGNORECASE,
    )

    text = re.sub(
        r"\b(?:\+91[-\s]?)?[6-9]\d{9}\b",
        "[PHONE]",
        text,
    )

    text = re.sub(
        r"\b\d{12}\b",
        "[ID]",
        text,
    )

    return text
