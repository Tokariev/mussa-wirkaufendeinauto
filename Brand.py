
class Brand(object):
    def fetch_brands(self, connection):
        cursor = connection.cursor()

        select = """SELECT * FROM brands"""
        cursor.execute(select)
        brands = cursor.fetchall()
        return brands