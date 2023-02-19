
class BodyType(object):
    def fetch_body_types(self, connection, built_year_id):
        cursor = connection.cursor()

        select = """SELECT * FROM body_types WHERE built_year_id = ?"""
        cursor.execute(select, (built_year_id,))
        body_types = cursor.fetchall()

        return body_types
