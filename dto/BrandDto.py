from dataclasses import dataclass

@dataclass(frozen=True)
class BrandDto:
    brand: str