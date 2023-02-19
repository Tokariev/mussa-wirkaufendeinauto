import sqlite3
from dao import get_connection
import requests
from dto.ModelDto import ModelDto


def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_models_if_exists = """DROP TABLE IF EXISTS models"""

    create_models_tab = """CREATE TABLE IF NOT EXISTS
                            models(
                                id INTEGER PRIMARY KEY,
                                model TEXT,
                                brand_id VARCHAR(3),
                                FOREIGN KEY(brand_id) REFERENCES brands(id))"""

    # cursor.execute(drop_models_if_exists)
    cursor.execute(create_models_tab)
    return connection


def read_all_brands_from_db(connection):
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM brands")
    rows = cursor.fetchall()
    return rows


def write_modell_to_db(connection, modeldto: ModelDto):
    cursor = connection.cursor()
    print(modeldto)
    try:
        insert = """INSERT OR IGNORE INTO models(model, brand_id)
                    VALUES (?,?)"""
        val = (modeldto.model, modeldto.brand_id)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()

def main():
    connection = create_db_if_not_exists()
    brands = read_all_brands_from_db(connection)
    for brand_row in brands:
        manufacturer = brand_row[0]
        brand = brand_row[1]
        print(manufacturer, brand)
        url = f"https://api-mcj.wkda.de/v1/cardata/types/main-types?manufacturer={manufacturer}&locale=de-DE&country=de"
        
        response = requests.get(url)
        models = response.json()

        for key, model in models["wkda"].items():
            modetdto = ModelDto(model, manufacturer)
            write_modell_to_db(connection, modetdto)


if __name__ == "__main__":
    main()