from dataclasses import dataclass


@dataclass(frozen=True)
class BodyTypeTextDto:
    body_type: str
    lang: str
    text: str