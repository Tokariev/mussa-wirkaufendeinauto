

#https://api-mcj.wkda.de/v1/cardata/types/body-types?manufacturer={manufacturer}&main-type=3er&built-year=2003&locale=de-DE&country=de


import sqlite3
import time
from dao import get_connection
import requests




def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_body_types_tab = """DROP TABLE IF EXISTS body_types"""
    drop_model_body_types_tab = """DROP TABLE IF EXISTS model_body_types"""

    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                    body_types(id INTEGER PRIMARY KEY,
                                               body_type VARCHAR(30))"""
#body_types
#+-------+-------------+
#| id    | body_type   |
#+-------+-------------+
#| 1007  | Cabrio      |
#| 1008  | Coupe       |
#+-------+-------------+

    create_model_body_types_tab = """CREATE TABLE IF NOT EXISTS
                                        model_body_types(
                                            id INTEGER PRIMARY KEY,
                                            model_id TEXT,
                                            built_year_id VARCHAR(4),
                                            body_type_id VARCHAR(4),
                                            FOREIGN KEY(built_year_id) REFERENCES built_years(id),
                                            FOREIGN KEY(body_type_id) REFERENCES body_types(id))"""

#model_body_types
#+----+----------+---------------+--------------+
#| id | model_id | built_year_id | body_type_id |
#+----+----------+---------------+--------------+
#| 1  | 1        | 2003          |1007          |
#| 2  | 1        | 2003          |1008          |
#+----+----------+---------------|--------------|

    cursor.execute(drop_body_types_tab)
    cursor.execute(drop_model_body_types_tab)
    cursor.execute(create_built_years_tab)
    cursor.execute(create_model_body_types_tab)

    return connection


def read_models_from_db(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM models"""
    cursor.execute(select)
    models = cursor.fetchall()
    return models

def read_built_years_by_model(connection, model_id) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM model_built_years WHERE model_id = ?"""
    cursor.execute(select, (model_id,))
    built_years = cursor.fetchall()
    return built_years

def write_body_type_to_db(connection, body_type_id, body_type):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO body_types(id, body_type)
                    VALUES (?, ?)"""
        val = (body_type_id, body_type)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def write_model_body_type_to_db(connection, model_id, built_year_id, body_type_id):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO model_body_types(model_id, built_year_id, body_type_id)
                    VALUES (?, ?, ?)"""
        val = (model_id, built_year_id, body_type_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)


def get_body_types(manufacturer, model, built_year):
    url = f"https://api-mcj.wkda.de/v1/cardata/types/body-types?manufacturer={manufacturer}&main-type={model}&built-year={built_year}&locale=de-DE&country=de"
    response = requests.get(url)
    data = response.json()
    return data["wkda"]

def run():
    connection = create_db_if_not_exists()
    models = read_models_from_db(connection)
    for model in models:
        model_id = model[0]
        model_built_years = read_built_years_by_model(connection, model_id)



        print(model[1])
        for built_year in model_built_years:
            year_id = built_year[2]
            model_name = model[1]
            manufatured_id = model[2]
            body_types = get_body_types(manufacturer=manufatured_id, model=model_name, built_year=year_id)

            for body_type in body_types:
                body_type_id = body_type
                body_type_value = body_types[body_type]
                write_body_type_to_db(connection, body_type_id=body_type_id, body_type=body_type_value)
                write_model_body_type_to_db(connection, model_id, year_id, body_type_id=body_type)
    connection.close()


if __name__ == '__main__':
    run()