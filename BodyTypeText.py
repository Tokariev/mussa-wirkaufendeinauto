
class BodyTypeText():
    def fetch_body_type_text(self, connection, body_type_id):
        cursor = connection.cursor()

        select = """SELECT * FROM body_types_text WHERE body_type = ?"""
        cursor.execute(select, (body_type_id,))
        body_type_text = cursor.fetchone()

        return body_type_text