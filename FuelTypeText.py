

class FuelTypeText(object):
    def fetch_fuel_type_text(self, connection, fuel_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM fuel_types_text WHERE fuel_type = ?"""
        cursor.execute(select, (fuel_type_id,))
        fuel_type_text = cursor.fetchone()

        return fuel_type_text