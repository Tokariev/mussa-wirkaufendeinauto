from dataclasses import dataclass
from typing import Type

@dataclass(frozen=True)
class ModelDto:
    model : str
    brand_id : str