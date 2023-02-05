

# https://www.digitalocean.com/community/tutorials/how-to-use-many-to-many-database-relationships-with-flask-and-sqlite

# https://api-mcj.wkda.de/v1/cardata/types/built-years?manufacturer=130&main-type=3er&locale=de-DE&country=de
# url = f"https://api-mcj.wkda.de/v1/cardata/types/built-years?manufacturer={manufacturer}&main-type={model}&locale=de-DE&country=de"


import sqlite3
import time
from dao import get_connection
import requests


def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_built_years_tab = """DROP TABLE IF EXISTS built_years"""
    drop_model_built_years_tab = """DROP TABLE IF EXISTS model_built_years"""

    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                built_years(id VARCHAR(4) PRIMARY KEY, year)"""

#model_built_years
#+----+----------+---------------+
#| id | model_id | built_year_id |
#+----+----------+---------------+
#| 1  | 1        | 2009          |
#| 2  | 1        | 2010          |
#+----+----------+---------------+

    create_model_built_years_tab = """CREATE TABLE IF NOT EXISTS
                           model_built_years(id INTEGER PRIMARY KEY, model_id TEXT, built_year_id VARCHAR(4), FOREIGN KEY(model_id) REFERENCES models(id), FOREIGN KEY(built_year_id) REFERENCES built_years(id))"""


    cursor.execute(drop_built_years_tab)
    cursor.execute(drop_model_built_years_tab)

    cursor.execute(create_built_years_tab)
    cursor.execute(create_model_built_years_tab)
    return connection


def read_models_from_db(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM models"""
    cursor.execute(select)
    models = cursor.fetchall()
    return models


def write_built_year_to_db(connection, id, year):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO built_years(id, year)
                    VALUES (?, ?)"""
        val = (id, year)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()

def assign_built_year_to_model(connection, model_id, built_year_id):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO model_built_years(model_id, built_year_id)
                    VALUES (?, ?)"""
        val = (model_id, built_year_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()

def main():
    connection = create_db_if_not_exists()
    models = read_models_from_db(connection)
    for model in models:
        model_id = model[0]
        model_name = model[1]
        manufacturer_id = model[2]
        print(manufacturer_id, model_name)
        url = f"https://api-mcj.wkda.de/v1/cardata/types/built-years?manufacturer={manufacturer_id}&main-type={model_name}&locale=de-DE&country=de"
        response = requests.get(url)

        years = response.json()
        for year_key, year in years["wkda"].items():
            write_built_year_to_db(connection, year_key, year)
            assign_built_year_to_model(connection, model_id, year_key)
            time.sleep(0.1)


if __name__ == "__main__":
    main()