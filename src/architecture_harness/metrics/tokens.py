from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class TokenMeasurement:
    count: int
    method: str


def measure_tokens(text: str) -> TokenMeasurement:
    """Use tiktoken when installed, otherwise a documented lexical estimate."""
    try:
        import tiktoken  # type: ignore
        encoding = tiktoken.get_encoding("o200k_base")
        return TokenMeasurement(len(encoding.encode(text)), "tiktoken:o200k_base")
    except ImportError:
        return TokenMeasurement(len(re.findall(r"[\w]+|[^\w\s]", text, re.UNICODE)), "lexical-estimate")

