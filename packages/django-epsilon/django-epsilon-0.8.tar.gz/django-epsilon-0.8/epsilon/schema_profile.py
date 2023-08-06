from schema import Schema, And

schema_profile = Schema({'first_name': And(str, len),
                         'last_name': And(str, len),
                         'date_of_birth': And(str, len),
                         'zip_code': And(str, len),
                         'email': And(str, len)
                         })
