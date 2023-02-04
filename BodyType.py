
class BodyType(object):
    def fetch_body_types(self, connection, model, built_year):
        cursor = connection.cursor()

        select = """SELECT * FROM model_body_types WHERE model_id = ? AND built_year_id = ?"""
        cursor.execute(select, (model, built_year))
        body_types = cursor.fetchall()

        return body_types
