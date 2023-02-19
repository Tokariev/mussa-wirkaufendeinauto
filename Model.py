
class Model(object):
    def fetch_models_by_brand(self, connection, manufacturer):
        cursor = connection.cursor()

        select = """SELECT * FROM models WHERE brand_id = ?"""
        cursor.execute(select, (manufacturer,))
        models = cursor.fetchall()
        return models