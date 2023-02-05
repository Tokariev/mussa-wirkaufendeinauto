from dto.BrandDto import BrandDto


class ModelDto:
    def __init__(self, model: str, brand_id: str) -> None:
        self.model = model
        self.brand_id = brand_id