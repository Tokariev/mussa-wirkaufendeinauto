
import sqlite3
from dao import get_connection
import requests
import asyncio
from dto.FuelTypeDto import FuelTypeDto, FuelTypeTextDto



def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_fuel_types_tab = """DROP TABLE IF EXISTS fuel_types"""

    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                    fuel_types(
                                        id INTEGER PRIMARY KEY,
                                        fuel_type INTEGER,
                                        body_type_id INTEGER,
                                        FOREIGN KEY(body_type_id) REFERENCES body_types(id) )"""

    drop_fuel_types_text_tab = """DROP TABLE IF EXISTS fuel_types_text"""
    create_fuel_types_text_tab = """CREATE TABLE IF NOT EXISTS
                                        fuel_types_text(
                                            fuel_type INTEGER,
                                            lang VARCHAR(2),
                                            text VARCHAR(30),
                                            PRIMARY KEY(fuel_type, lang) )"""

    # cursor.execute(drop_fuel_types_tab)
    # cursor.execute(drop_fuel_types_text_tab)
    cursor.execute(create_built_years_tab)
    cursor.execute(create_fuel_types_text_tab)

    return connection


def fetch_single_model_row(connection, model_id) -> str:
    cursor = connection.cursor()

    select = """SELECT * FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    model = cursor.fetchone()
    return model


async def write_fuel_type_to_db(connection, fuel_type_dto: FuelTypeDto):
    cursor = connection.cursor()

    insert = """INSERT INTO fuel_types (fuel_type, body_type_id) VALUES (?, ?)"""
    cursor.execute(insert, (fuel_type_dto.fuel_type, fuel_type_dto.body_type_id))
    connection.commit()


def fetch_body_types(connection):
    cursor = connection.cursor()

    select = """SELECT * FROM body_types"""
    cursor.execute(select)
    rows = cursor.fetchall()
    return rows


def fetch_single_built_year_row(connection, id):
    cursor = connection.cursor()

    select = """SELECT * FROM built_years WHERE id = ?"""
    cursor.execute(select, (id,))
    built_year = cursor.fetchone()
    return built_year

async def write_fuel_type_text_to_db(connection, fuel_type_text: FuelTypeTextDto):
    cursor = connection.cursor()

    insert = """INSERT OR IGNORE INTO fuel_types_text (fuel_type, lang, text) VALUES (?, ?, ?)"""
    cursor.execute(insert, (fuel_type_text.fuel_type, fuel_type_text.lang, fuel_type_text.text))
    connection.commit()

def check_if_fuel_types_already_assigned_to_body_type(connection, body_type_id):
    cursor = connection.cursor()

    select = """SELECT * FROM fuel_types WHERE body_type_id = ?"""
    cursor.execute(select, (body_type_id,))
    rows = cursor.fetchall()
    if len(rows) > 0:
        return True

async def fetch_fuel_types(body_type, built_year, model, brand_id):
    url = f"https://api-mcj.wkda.de/v1/cardata/types/fuel-types?manufacturer={brand_id}&main-type={model}&built-year={built_year}&body-type={body_type}&locale=de-DE&country=de"
    fuel_types = requests.get(url).json()
    return fuel_types

async def main():
    connection = create_db_if_not_exists()

    body_types = fetch_body_types(connection)
    count = 0
    for body_type_row in body_types:
        body_type_id = body_type_row[0]
        body_type = body_type_row[1]
        buily_yead_id = body_type_row[2]

        built_year_row = fetch_single_built_year_row(connection, buily_yead_id)
        built_year = built_year_row[1]
        moel_id = built_year_row[2]

        model_row = fetch_single_model_row(connection, moel_id)
        model = model_row[1]

        brand_id = model_row[2]

        if check_if_fuel_types_already_assigned_to_body_type(connection, body_type_id):
            count += 1
            continue

        fuel_types = await fetch_fuel_types(body_type, built_year, model, brand_id)
        await asyncio.sleep(0.1)

        for fuel_key, value in fuel_types["wkda"].items():
            pass
            fuel_type_dto = FuelTypeDto(fuel_key, body_type_id)
            task_1 = asyncio.create_task(write_fuel_type_to_db(connection, fuel_type_dto))

            fuel_type_text_dto = FuelTypeTextDto(fuel_key, "de", value)
            task_2 = asyncio.create_task(write_fuel_type_text_to_db(connection, fuel_type_text_dto))


        count += 1
        print(f"Body types count: {count} / {len(body_types)}")



if __name__ == "__main__":
    asyncio.run(main())