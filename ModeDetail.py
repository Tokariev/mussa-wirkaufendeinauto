
class ModelDetail(object):
    def fetch_model_details(self, connection, body_type_fuel_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM body_type_fuel_type_model_details WHERE body_type_fuel_type_id = ?"""
        cursor.execute(select, (body_type_fuel_type_id,))
        model_details = cursor.fetchall()
        return model_details