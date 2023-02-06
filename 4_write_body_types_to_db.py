

#https://api-mcj.wkda.de/v1/cardata/types/body-types?manufacturer={manufacturer}&main-type=3er&built-year=2003&locale=de-DE&country=de


import sqlite3
import time
from dao import get_connection
import requests
from dto.BodyTypeDto import BodyTypeDto, BodyTypeTextDto




def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_body_types_tab = """DROP TABLE IF EXISTS body_types"""
    drop_body_types_text_tab = """DROP TABLE IF EXISTS body_types_text"""

    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                    body_types(
                                        id INTEGER PRIMARY KEY,
                                        body_type INTEGER,
                                        built_year_id INTEGER,
                                        FOREIGN KEY(built_year_id) REFERENCES built_years(id) )"""

    create_body_types_text_tab = """CREATE TABLE IF NOT EXISTS
                                        body_types_text(
                                            body_type INTEGER,
                                            lang VARCHAR(2),
                                            text VARCHAR(30),
                                            PRIMARY KEY(body_type, lang) )"""

    # cursor.execute(drop_body_types_tab)
    # cursor.execute(drop_body_types_text_tab)
    cursor.execute(create_built_years_tab)
    cursor.execute(create_body_types_text_tab)

    return connection


def write_body_type_to_db(connection, body_type_dto: BodyTypeDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT INTO body_types(body_type, built_year_id)
                    VALUES (?, ?)"""
        val = (body_type_dto.body_type, body_type_dto.built_year_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def read_built_years(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM built_years"""
    cursor.execute(select)
    built_years = cursor.fetchall()
    return built_years

def fetch_brand_id(connection, model_id: int) -> str:
    cursor = connection.cursor()

    select = """SELECT brand_id FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    brand_id = cursor.fetchone()
    return brand_id[0]

def write_body_type_text_to_db(connection, body_type_text_dto: BodyTypeTextDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO body_types_text(body_type, lang, text)
                    VALUES (?, ?, ?)"""
        val = (body_type_text_dto.body_type, body_type_text_dto.lang, body_type_text_dto.text)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def fetch_model(connection, model_id: int) -> str:
    cursor = connection.cursor()

    select = """SELECT model FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    model = cursor.fetchone()
    return model[0]

def check_if_body_types_already_assigned_to_built_year_id(connection, built_year_id: int):
    cursor = connection.cursor()

    select = """SELECT * FROM body_types WHERE built_year_id = ?"""
    cursor.execute(select, (built_year_id,))
    body_types = cursor.fetchall()
    if len(body_types) > 0:
        return True

def main():
    connection = create_db_if_not_exists()

    built_years = read_built_years(connection)
    count = 0
    for built_year_row in built_years:
        built_year_id = built_year_row[0]
        built_year = built_year_row[1]
        model_id = built_year_row[2]
        model = fetch_model(connection, model_id)
        brand_id = fetch_brand_id(connection, model_id)

        if check_if_body_types_already_assigned_to_built_year_id(connection, built_year_id):
            count += 1
            continue

        url = f"https://api-mcj.wkda.de/v1/cardata/types/body-types?manufacturer={brand_id}&main-type={model}&built-year={built_year}&locale=de-DE&country=de"
        response = requests.get(url)
        data = response.json()
        body_types = data["wkda"]

        for key, value in body_types.items():
            body_type_dto = BodyTypeDto(body_type=key, built_year_id=built_year_id)
            write_body_type_to_db(connection, body_type_dto)

            body_type_text_dto = BodyTypeTextDto(body_type=key, lang="de", text=value)
            write_body_type_text_to_db(connection, body_type_text_dto)

        count += 1
        print(f"Built year count: {count} / {len(built_years)}")

    connection.close()


if __name__ == '__main__':
    main()