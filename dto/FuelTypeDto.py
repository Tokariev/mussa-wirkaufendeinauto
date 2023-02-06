from dataclasses import dataclass


@dataclass(frozen=True)
class FuelTypeDto:
    fuel_type: int
    body_type_id: int


@dataclass(frozen=True)
class FuelTypeTextDto:
    fuel_type: int
    lang: str
    text: str