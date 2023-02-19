
class ModelVariants(object):
    def fetch_model_variants(self, connection, fuel_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM model_variants WHERE fuel_type_id = ?"""
        cursor.execute(select, (fuel_type_id,))
        model_variants = cursor.fetchall()

        return model_variants