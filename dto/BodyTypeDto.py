from dataclasses import dataclass


@dataclass(frozen=True)
class BodyTypeDto:
    body_type: str
    built_year_id: int