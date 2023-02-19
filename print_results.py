
from Brand import Brand
from Model import Model
from BuiltYear import BuiltYear
from BodyType import BodyType
from BodyTypeText import BodyTypeText
from FuelType import FuelType
from FuelTypeText import FuelTypeText
from ModelVariants import ModelVariants
from ModelVariantText import ModelVariantText
from EnginePower import EnginePower
from dao import get_connection


if __name__ == '__main__':
    conn = get_connection()

    # 1 Brands
    brands = Brand().fetch_brands(conn)
    for brand in brands:
        if brand[1] == 'BMW':
            print(brand[1])
            brand_id = brand[0]
            break

    # 2 Models
    models = Model().fetch_models_by_brand(conn, brand_id)
    for model in models:
        if model[1] == '3er':
            print(model[1])
            model_id = model[0]
            break

    # 3 Built years
    built_years = BuiltYear().fetch_built_years(conn, model_id)

    for year in built_years:
        if year[1] == 2003:
            print(year[1])
            built_year_id = year[0]
            break

    # 4 Bauformen
    body_types = BodyType().fetch_body_types(conn, built_year_id)
    for body_type in body_types:
        text = BodyTypeText().fetch_body_type_text(conn, body_type[1])
        if text[2] == 'Limousine':
            print(text[2])
            body_type_id = body_type[0]
            break

    # 5 Kraftstoff
    fuel_types = FuelType().fetch_fuel_types(conn, body_type_id)
    for fuel_type in fuel_types:
        text = FuelTypeText().fetch_fuel_type_text(conn, fuel_type[1])
        if text[2] == 'Benzin':
            print(text[2])
            fuel_type_id = fuel_type[0]
            break

    # 6 Model variants
    model_variants = ModelVariants().fetch_model_variants(conn, fuel_type_id)
    for model_variant in model_variants:
        if model_variant[1] == '316i':
            print(model_variant[1])
            model_variant_id = model_variant[0]
            break

    # 7 Engine power
    engine_powers = EnginePower().fetch_engine_powers(conn, model_variant_id)
    for engine_power in engine_powers:
        print(engine_power)


