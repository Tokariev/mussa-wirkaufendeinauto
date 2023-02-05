import json
import sqlite3
import requests
from dao import get_connection
from dto.BrandDto import BrandDto

def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    drop_brands_tab = """DROP TABLE IF EXISTS brands"""
    create_brands_tab = """CREATE TABLE IF NOT EXISTS
                            brands(
                                id VARCHAR(3) PRIMARY KEY,
                                brand VARCHAR(30))"""

    cursor.execute(drop_brands_tab)
    cursor.execute(create_brands_tab)
    return connection


def write_marke_to_db(connection, branddto: BrandDto):
    cursor = connection.cursor()

    try:
        insert = """INSERT INTO brands(id, brand)
                    VALUES (?, ?)"""
        val = (branddto.id, branddto.brand)
        cursor.execute(insert, val)
        connection.commit()
    except sqlite3.Error as error:
        print("Failed to insert data into sqlite table", error)
    finally:
        if cursor:
            cursor.close()


if __name__ == "__main__":
    with open('marke.json') as f:
        data = json.load(f)
        wkda = data["https://api-mcj.wkda.de/v1/cardata/types/manufacturers-{\"locale\":\"de-DE\",\"country\":\"de\"}"]["response"]["result"]["wkda"]


    connection = create_db_if_not_exists()
    marke_modelle = []
    for manufacturer, brand in wkda.items():
        branddto = BrandDto(manufacturer, brand)
        write_marke_to_db(connection, branddto)