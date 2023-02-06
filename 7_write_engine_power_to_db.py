import asyncio
import sqlite3
import time
from dao import get_connection
import requests
from dto.EnginePowerDto import EnginePowerDto
# Horse power
# https://api-mcj.wkda.de/v1/cardata/types/kw?manufacturer=130&main-type=3er&built-year=2011&body-type=1008&fuel-type=1039&main-type-detail=320i&locale=de-DE&country=de

def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_engine_power_tab = """DROP TABLE IF EXISTS engine_power"""
    create_engine_power_tab = """CREATE TABLE IF NOT EXISTS
                                    engine_power(
                                        id INTEGER PRIMARY KEY,
                                        engine_power INTEGER,
                                        model_variant_id INTEGER,
                                        FOREIGN KEY(model_variant_id) REFERENCES model_variants(id) )"""

    cursor.execute(drop_engine_power_tab)
    cursor.execute(create_engine_power_tab)

    return connection

def fetch_single_fuel_type(connection, fuel_type_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM fuel_types WHERE id = ?"""
    cursor.execute(select, (fuel_type_id,))
    fuel_type = cursor.fetchone()
    return fuel_type

def fetch_model_variants(connection) -> list:
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM model_variants")
    model_variants = cursor.fetchall()
    return model_variants

def fetch_single_body_type(connection, body_type_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM body_types WHERE id = ?"""
    cursor.execute(select, (body_type_id,))
    body_type = cursor.fetchone()
    return body_type

def fetch_single_built_year(connection, built_year_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM built_years WHERE id = ?"""
    cursor.execute(select, (built_year_id,))
    built_year = cursor.fetchone()
    return built_year

def fetch_single_model(connection, model_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    model = cursor.fetchone()
    return model

def checkif_model_variant_id_already_assigned_horse_power(connection, model_variant_id) -> bool:
    cursor = connection.cursor()
    select = """SELECT * FROM engine_power WHERE model_variant_id = ?"""
    cursor.execute(select, (model_variant_id,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return True

def write_engine_power_to_db(connection, engine_power_dto: EnginePowerDto):
    cursor = connection.cursor()
    insert = """INSERT INTO engine_power(engine_power, model_variant_id) VALUES (?, ?)"""
    cursor.execute(insert, (engine_power_dto.engine_power, engine_power_dto.model_variant_id))
    connection.commit()


def main():
    connection = create_db_if_not_exists()

    model_variants = fetch_model_variants(connection)
    count = 0
    for model_variant_row in model_variants:
        model_variand_id = model_variant_row[0]
        model_variant = model_variant_row[1]
        fuel_type_id = model_variant_row[2]

        fuel_type_row = fetch_single_fuel_type(connection, fuel_type_id)
        fuel_type = fuel_type_row[1]
        body_type_id = fuel_type_row[2]

        body_type_row = fetch_single_body_type(connection, body_type_id)
        body_type = body_type_row[1]
        built_year_id = body_type_row[2]

        built_year_row = fetch_single_built_year(connection, built_year_id)
        built_year = built_year_row[1]
        model_id = built_year_row[2]

        model_row = fetch_single_model(connection, model_id)
        model = model_row[1]
        brand = model_row[2]

        if checkif_model_variant_id_already_assigned_horse_power(connection, model_variand_id):
            count += 1
            continue

        url = f"https://api-mcj.wkda.de/v1/cardata/types/kw?manufacturer={brand}&main-type={model}&built-year={built_year}&body-type={body_type}&fuel-type={fuel_type}&main-type-detail={model_variant}&locale=de-DE&country=de"
        response = requests.get(url)
        engine_power = response.json()

        for key, value in engine_power["wkda"].items():
            horse_power_dto = EnginePowerDto(key, model_variand_id)
            write_engine_power_to_db(connection, horse_power_dto)


        count += 1
        print(f"Model variants: {count} / {len(model_variants)}")
if __name__ == "__main__":
    main()