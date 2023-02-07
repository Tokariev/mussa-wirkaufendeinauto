
import sqlite3
from dao import get_connection
import requests
from dto.BuiltYearDto import BuiltYearDto


def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_built_years_tab = """DROP TABLE IF EXISTS built_years"""


    create_built_years_tab = """CREATE TABLE IF NOT EXISTS
                                built_years(
                                    id INTEGER PRIMARY KEY,
                                    year INTEGER,
                                    model_id INTEGER,
                                    FOREIGN KEY(model_id) REFERENCES models(id))"""

    # cursor.execute(drop_built_years_tab)
    cursor.execute(create_built_years_tab)
    return connection


def read_models_from_db(connection) -> list:
    cursor = connection.cursor()

    select = """SELECT * FROM models"""
    cursor.execute(select)
    models = cursor.fetchall()
    return models


def write_built_year_to_db(connection, builtYearDto: BuiltYearDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT INTO built_years(year, model_id)
                    VALUES (?, ?)"""
        val = (builtYearDto.year, builtYearDto.model_id)
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
            builtYearDto = BuiltYearDto(year, model_id)
            write_built_year_to_db(connection, builtYearDto)
            # assign_built_year_to_model(connection, model_id, year_key)


if __name__ == "__main__":
    main()