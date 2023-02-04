

# rerquest
# https://api-mcj.wkda.de/v1/cardata/types/fuel-types?manufacturer=130&main-type=3er&built-year=2003&body-type=1025&locale=de-DE&country=de

# response
# { 1039: "Benzin", 1040: "Diesel" }


import sqlite3
import time
from dao import get_connection
import requests




def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_model_details_tab = """DROP TABLE IF EXISTS model_details"""

    create_model_details_tab = """CREATE TABLE IF NOT EXISTS
                                    model_details(
                                        id INTEGER PRIMARY KEY,
                                        model_detail_extern_key VARCHAR(30),
                                        model_detail VARCHAR(30))"""
#model_details
#+--------+-------------------------+--------------+
#| id     | model_detail_extern_key | model_detail |
#+--------+-------------------------+--------------+
#| 1      | 318Ci                   | 318Ci        |
#| 2      | 320Ci                   | 320Ci        |
#+--------+-------------------------+--------------+

    drop_fuel_type_model_details_tab = """DROP TABLE IF EXISTS fuel_type_model_details"""
    create_fuel_type_model_details_tab = """CREATE TABLE IF NOT EXISTS
                                                body_type_fuel_type_model_details(
                                                    id INTEGER PRIMARY KEY,
                                                    body_type_fuel_type_id INTEGER,
                                                    model_detail_id INTEGER,
                                                    FOREIGN KEY(body_type_fuel_type_id) REFERENCES body_type_fuel_types(id),
                                                    FOREIGN KEY(model_detail_id) REFERENCES model_details(id))"""

#body_type_fuel_type_model_details
#+----+------------------------+---------------+
#| id | body_type_fuel_type_id | fuel_type_id  |
#+----+------------------------+---------------+
#|1   | 1                      | 1007          |
#|2   | 1                      | 1008          |
#+----|------------------------|---------------|

    cursor.execute(drop_model_details_tab)
    cursor.execute(drop_fuel_type_model_details_tab)
    cursor.execute(create_model_details_tab)
    cursor.execute(create_fuel_type_model_details_tab)

    return connection

def read_model_body_type_from_db(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM model_body_types"""

    cursor.execute(select)
    rows = cursor.fetchall()
    return rows


def fetch_single_model_name_model_id(connection, model_id) -> str:
    cursor = connection.cursor()

    select = """SELECT model FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    model = cursor.fetchone()
    return model[0]


def write_model_details_to_db(connection, model_detail_extern_key, model_detail):
    cursor = connection.cursor()

    select = """SELECT * FROM model_details WHERE model_detail_extern_key = ? AND model_detail = ?"""
    cursor.execute(select, (model_detail_extern_key, model_detail))
    model_detail_row = cursor.fetchone()
    if model_detail_row is not None:
        return model_detail_row[0] #Id

    insert = """INSERT INTO model_details(model_detail_extern_key, model_detail) VALUES (?, ?)"""
    cursor.execute(insert, (model_detail_extern_key, model_detail))
    connection.commit()
    return cursor.lastrowid


def fetch_manufacturer_id_by_model_id(connection, model_id) -> str:
    cursor = connection.cursor()

    select = """SELECT manufacturer_id FROM models WHERE id = ?"""
    cursor.execute(select, (model_id,))
    manufacture_id = cursor.fetchone()
    return manufacture_id[0]

def fetch_body_types_by_year_and_model_id(connection, built_year_id, model_id) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM model_body_types WHERE built_year_id = ? AND model_id = ?"""
    cursor.execute(select, (built_year_id, model_id))
    rows = cursor.fetchall()
    return rows

def fetch_body_type_fuel_types(connection, model_body_type_id):
    cursor = connection.cursor()

    select = """SELECT * FROM body_type_fuel_types WHERE model_body_type_id = ?"""
    cursor.execute(select, (model_body_type_id,))
    fuel_types = cursor.fetchall()
    return fuel_types

def assign_model_details_to_model_body_types_and_fuel_variant(connection, body_type_fuel_type_id, model_variant_key):
    cursor = connection.cursor()

    insert = """INSERT INTO body_type_fuel_type_model_details(body_type_fuel_type_id, model_detail_id) VALUES (?, ?)"""
    cursor.execute(insert, (body_type_fuel_type_id, model_variant_key))
    connection.commit()

def run():
    connection = create_db_if_not_exists()
    model_body_types = read_model_body_type_from_db(connection)

    count = 0
    for model_body_type in model_body_types:
        model_body_type_id = model_body_type[0]
        model_id = model_body_type[1]
        manufacturer_id = fetch_manufacturer_id_by_model_id(connection, model_id)
        model_name = fetch_single_model_name_model_id(connection, model_id)
        buily_yead_id = model_body_type[2]

        body_types = fetch_body_types_by_year_and_model_id(connection, buily_yead_id, model_id)
        for body_type in body_types:
            body_type_id = body_type[3]
            body_type_fuel_types = fetch_body_type_fuel_types(connection, model_body_type_id)
            for body_type_ful_type_row in body_type_fuel_types:
                body_type_fuel_type_id = body_type_ful_type_row[0]
                fuel_type = body_type_ful_type_row[2]
                url = f"https://api-mcj.wkda.de/v1/cardata/types/main-types-details?manufacturer={manufacturer_id}&main-type={model_name}&built-year={buily_yead_id}&body-type={body_type_id}&fuel-type={fuel_type}&short-form=false&locale=de-DE&country=de"
                model_variants = requests.get(url).json()

                for model_variant_key, value in model_variants["wkda"].items():
                    model_variant_internal_id = write_model_details_to_db(connection, model_detail_extern_key=model_variant_key, model_detail=value)
                    assign_model_details_to_model_body_types_and_fuel_variant(connection, body_type_fuel_type_id, model_variant_internal_id)
        count += 1
        print(f"count: {count} / {len(model_body_types)}")

if __name__ == "__main__":
    run()