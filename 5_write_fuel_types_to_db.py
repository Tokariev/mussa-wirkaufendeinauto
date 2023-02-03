
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

    drop_fuel_types_tab = """DROP TABLE IF EXISTS fuel_types"""

    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                    fuel_types(
                                        id INTEGER PRIMARY KEY,
                                        fuel_type VARCHAR(30))"""
#fuel_types
#+-------+-------------+
#| id    | fuel_type   |
#+-------+-------------+
#| 1039  | Benzin      |
#| 1040  | Diesel      |
#+-------+-------------+
    drop_body_type_fuel_types_tab = """DROP TABLE IF EXISTS body_type_fuel_types"""
    create_body_type_fuel_types_tab = """CREATE TABLE IF NOT EXISTS
                                        body_type_fuel_types(
                                            id INTEGER PRIMARY KEY,
                                            model_body_type_id INTEGER,
                                            fuel_type_id INTEGER,
                                            FOREIGN KEY(model_body_type_id) REFERENCES model_body_types(id),
                                            FOREIGN KEY(fuel_type_id) REFERENCES fuel_types(id))"""

#body_type_fuel_types
#+----+--------------------+---------------+
#| id | model_body_type_id | fuel_type_id  |
#+----+--------------------+---------------+
#|1   | 1                  | 1007          |
#|2   | 1                  | 1008          |
#+----|--------------------|---------------|

    cursor.execute(drop_fuel_types_tab)
    cursor.execute(drop_body_type_fuel_types_tab)
    cursor.execute(create_built_years_tab)
    cursor.execute(create_body_type_fuel_types_tab)

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


def write_fuel_type_to_db(connection, key, fuel_type):
    cursor = connection.cursor()

    insert = """INSERT OR IGNORE INTO fuel_types (id, fuel_type) VALUES (?, ?)"""
    cursor.execute(insert, (key, fuel_type))
    connection.commit()

def assign_fuel_type_to_model_body_types(connection, model_body_type_id, fuel_type_id):
    cursor = connection.cursor()

    insert = """INSERT OR IGNORE INTO body_type_fuel_types (model_body_type_id, fuel_type_id) VALUES (?, ?)"""
    cursor.execute(insert, (model_body_type_id, fuel_type_id))
    connection.commit()


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

            url = f"https://api-mcj.wkda.de/v1/cardata/types/fuel-types?manufacturer={manufacturer_id}&main-type={model_name}&built-year={buily_yead_id}&body-type={body_type_id}&locale=de-DE&country=de"
            fuel_types = requests.get(url).json()

            for fuel_key, value in fuel_types["wkda"].items():
                write_fuel_type_to_db(connection, fuel_key, value)
                assign_fuel_type_to_model_body_types(connection, model_body_type_id, fuel_key)
        count += 1
        print(f"count: {count} / {len(model_body_types)}")

if __name__ == "__main__":
    run()