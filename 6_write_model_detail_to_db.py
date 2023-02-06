

# rerquest
# https://api-mcj.wkda.de/v1/cardata/types/fuel-types?manufacturer=130&main-type=3er&built-year=2003&body-type=1025&locale=de-DE&country=de

# response
# { 1039: "Benzin", 1040: "Diesel" }


import asyncio
import sqlite3
import time
from dao import get_connection
import requests
from dto.ModelVariantDto import ModelVariantDto, ModelVariantTextDto



def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_model_variants_tab = """DROP TABLE IF EXISTS model_variants"""
    create_model_variants_tab = """CREATE TABLE IF NOT EXISTS
                                    model_variants(
                                        id INTEGER PRIMARY KEY,
                                        model_variant VARCHAR(30),
                                        fuel_type_id VARCHAR(30),
                                        FOREIGN KEY(fuel_type_id) REFERENCES fuel_types(id) )"""


    drop_model_variants_text_tab = """DROP TABLE IF EXISTS fuel_type_model_details"""
    create_model_variants_text_tab = """CREATE TABLE IF NOT EXISTS
                                                model_variants_text(
                                                    model_variant VARCHAR(30),
                                                    lang VARCHAR(2),
                                                    text VARCHAR(30),
                                                    PRIMARY KEY(model_variant, lang) )"""

    cursor.execute(drop_model_variants_tab)
    cursor.execute(drop_model_variants_text_tab)
    cursor.execute(create_model_variants_tab)
    cursor.execute(create_model_variants_text_tab)

    return connection


async def write_model_variants_to_db(connection, modelVariantDto: ModelVariantDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT INTO model_variants(model_variant, fuel_type_id)
                    VALUES (?, ?)"""
        val = (modelVariantDto.model_variant, modelVariantDto.fuel_type_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()


def fetch_fuel_types(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM fuel_types"""
    cursor.execute(select)
    fuel_types = cursor.fetchall()
    return fuel_types

def fetch_single_body_type(connection, body_type_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM body_types WHERE id = ?"""
    cursor.execute(select, (body_type_id,))
    body_type = cursor.fetchone()
    return body_type

def fetch_built_year(connection, built_year_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM built_years WHERE id = ?"""
    cursor.execute(select, (built_year_id,))
    built_year = cursor.fetchone()
    return built_year

def fetch_model_row(connection, model_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    model = cursor.fetchone()
    return model

def check_if_model_variants_already_assigned_to_fuel_type(connection, fuel_type_id) -> bool:
    cursor = connection.cursor()

    select = """SELECT * FROM model_variants WHERE fuel_type_id = ?"""
    cursor.execute(select, (fuel_type_id,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return True

async def write_model_variants_text_to_db(connection, model_variant_text_dto: ModelVariantTextDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO model_variants_text(model_variant, lang, text)
                    VALUES (?, ?, ?)"""
        val = (model_variant_text_dto.model_variant, model_variant_text_dto.lang, model_variant_text_dto.text)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()


async def fetch_model_variants(fuel_type, body_type, built_year, brand, model):
    url = f"https://api-mcj.wkda.de/v1/cardata/types/main-types-details?manufacturer={brand}&main-type={model}&built-year={built_year}&body-type={body_type}&fuel-type={fuel_type}&short-form=false&locale=de-DE&country=de"
    model_variants = requests.get(url).json()
    return model_variants



async def main():
    connection = create_db_if_not_exists()

    fuel_types = fetch_fuel_types(connection)
    count = 0
    for fuel_type_row in fuel_types:
        fuel_type_id = fuel_type_row[0]
        fuel_type = fuel_type_row[1]
        body_type_id = fuel_type_row[2]

        body_type_row = fetch_single_body_type(connection, body_type_id)
        body_type = body_type_row[1]
        built_year_id = fuel_type_row[2]

        built_year_row = fetch_built_year(connection, built_year_id)
        built_year = built_year_row[1]
        model_id = built_year_row[2]

        model_row = fetch_model_row(connection, model_id)
        brand = model_row[2]
        model = model_row[1]


        if check_if_model_variants_already_assigned_to_fuel_type(connection, fuel_type_id):
            count += 1
            continue

        model_variants = await fetch_model_variants(fuel_type, body_type, built_year, brand, model)

        for key, value in model_variants["wkda"].items():
            model_variant_dto = ModelVariantDto(key, fuel_type_id)
            task_1 = asyncio.create_task(write_model_variants_to_db(connection, model_variant_dto))

            model_variant_text_dto = ModelVariantTextDto(key, 'de', value)
            task_2 = asyncio.create_task(write_model_variants_text_to_db(connection, model_variant_text_dto))

            await asyncio.sleep(0.05)

        count += 1
        print(f"Fuel types count: {count} / {len(fuel_types)}")


if __name__ == "__main__":
    asyncio.run(main())