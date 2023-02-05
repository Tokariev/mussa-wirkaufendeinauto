from dataclasses import dataclass


@dataclass(frozen=True)
class BodyTypeTextDto:
    body_type: str
    locale: str
    text: str