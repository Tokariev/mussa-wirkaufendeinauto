class EnginePower(object):
    def fetch_engine_powers(self, connection, model_variant_id):
        cursor = connection.cursor()

        select = """SELECT * FROM engine_power WHERE model_variant_id = ?"""
        cursor.execute(select, (model_variant_id,))
        engine_powers = cursor.fetchall()

        return engine_powers