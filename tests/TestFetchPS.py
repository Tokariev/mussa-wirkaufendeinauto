import unittest
import os


# https://api-mcj.wkda.de/v1/cardata/types/main-types-sub?manufacturer=060&main-type=A6&built-year=2022&body-type=1025&fuel-type=1040&main-type-detail=50 TDI&kw=180.00&gear-type=1141&door-count=4&short-form=false&locale=de-DE&country=de

# Input data:
# manufacturer_id = 060
# model_name = A6
# built_year = 2022
# body_type_id = 1025
# fuel_type = 1040


# Output data:
# model_detail = 45 TDI
# model_detail = 50 TDI

