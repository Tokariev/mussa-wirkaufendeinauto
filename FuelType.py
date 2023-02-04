

class FuelType(object):
    def fetch_fuel_types(self, connection, model_body_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM body_type_fuel_types WHERE model_body_type_id = ?"""
        cursor.execute(select, (model_body_type_id,))
        fuel_types = cursor.fetchall()
        print(fuel_types)
        return fuel_types
