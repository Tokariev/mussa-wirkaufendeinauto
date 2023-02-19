

class FuelType(object):
    def fetch_fuel_types(self, connection, body_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM fuel_types WHERE body_type_id = ?"""
        cursor.execute(select, (body_type_id,))
        fuel_types = cursor.fetchall()

        return fuel_types
