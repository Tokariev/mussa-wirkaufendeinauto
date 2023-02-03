import json
import sqlite3
import requests
from dao import get_connection

def create_db_if_not_exists() -> sqlite3.Connection:
    connection = get_connection()
    cursor = connection.cursor()

    create_brands_tab = """CREATE TABLE IF NOT EXISTS
                            brands(manufacturer VARCHAR(3) PRIMARY KEY, brand)"""

    cursor.execute(create_brands_tab)
    return connection


def write_marke_to_db(connection, manufacturer, brand):
    cursor = connection.cursor()

    try:
        insert = """INSERT OR IGNORE INTO brands(manufacturer, brand)
                    VALUES (?, ?)"""
        val = (manufacturer, brand)
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
        write_marke_to_db(connection, manufacturer, brand)