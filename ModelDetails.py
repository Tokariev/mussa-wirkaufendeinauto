

class ModelDetails:
    def __init__(self, brand, model, built_year, body_type, fuel_type):
        self.brand = brand
        self.model = model
        self.built_year = built_year
        self.body_type = body_type
        self.fuel_type = fuel_type

    def fetch_model_details(self, connection):
        cursor = connection.cursor()

        select = """SELECT * FROM model_details WHERE model_id = ?"""
        cursor.execute(select, (self.model_id,))
        model_details = cursor.fetchall()
        return model_details