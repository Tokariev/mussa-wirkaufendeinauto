
class Model(object):
    def fetch_models_by_manufacturer(self, connection, manufacturer):
        cursor = connection.cursor()

        select = """SELECT * FROM models WHERE manufacturer_id = ?"""
        cursor.execute(select, (manufacturer,))
        models = cursor.fetchall()
        return models