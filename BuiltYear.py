
class BuiltYear(object):
    def fetch_built_years(self, connection, model):
        cursor = connection.cursor()

        select = """SELECT * FROM model_built_years WHERE model_id = ?"""
        cursor.execute(select, (model,))
        built_years = cursor.fetchall()

        return built_years