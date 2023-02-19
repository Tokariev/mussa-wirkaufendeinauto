
class ModelVariantText(object):
    def fetch_model_variant_text(self, connection, model_variant):
        cursor = connection.cursor()

        select = """SELECT * FROM model_variants_text WHERE model_variant = ?"""
        cursor.execute(select, (model_variant,))
        model_variants = cursor.fetchone()

        return model_variants