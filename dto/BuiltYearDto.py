from dataclasses import dataclass


@dataclass(frozen=True)
class BuiltYearDto:
    year: int
    model_id: int