from dataclasses import dataclass


@dataclass(frozen=True)
class ModelVariantDto:
    model_variant: str
    fuel_type_id: int


@dataclass(frozen=True)
class ModelVariantTextDto:
    model_variant: str
    lang: str
    text: str