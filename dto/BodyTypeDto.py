from dataclasses import dataclass


@dataclass(frozen=True)
class BodyTypeDto:
    body_type: int
    built_year_id: int


@dataclass(frozen=True)
class BodyTypeTextDto:
    body_type: int
    lang: str
    text: str