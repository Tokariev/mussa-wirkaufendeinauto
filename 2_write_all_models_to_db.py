import sqlite3
from dao import get_connection
import requests


def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_models_if_exists = """DROP TABLE IF EXISTS models"""

    create_marken_tab = """CREATE TABLE IF NOT EXISTS
                            models(id INTEGER PRIMARY KEY, model TEXT, manufacturer_id VARCHAR(3), FOREIGN KEY(manufacturer_id) REFERENCES marken(manufacturer))"""

    cursor.execute(drop_models_if_exists)
    cursor.execute(create_marken_tab)
    return connection


def read_all_brands_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM brands")
    rows = cursor.fetchall()
    return rows


def write_modell_to_db(connection, modell, manufacturer_id):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO models(model, manufacturer_id)
                    VALUES (?,?)"""
        val = (modell, manufacturer_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()

def run():
    connection = create_db_if_not_exists()
    brands = read_all_brands_from_db(connection)
    for brand in brands:
        manufacturer = brand[0]
        print(manufacturer, brand[1])
        url = f"https://api-mcj.wkda.de/v1/cardata/types/main-types?manufacturer={manufacturer}&locale=de-DE&country=de"
        response = requests.get(url)

        models = response.json()
        for key, model in models["wkda"].items():
            print(key, model)
            write_modell_to_db(connection, model, manufacturer)


if __name__ == "__main__":
    run()