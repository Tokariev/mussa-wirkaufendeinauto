from dataclasses import dataclass

@dataclass(frozen=True)
class EnginePowerDto:
    engine_power: int
    model_variant_id: str
