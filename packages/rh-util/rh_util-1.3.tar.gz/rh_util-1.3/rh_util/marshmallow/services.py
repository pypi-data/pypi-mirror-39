from marshmallow import fields, missing


class SmartNested(fields.Nested):
    
    def _validate_missing(self, value):
        if value is missing and getattr(self, 'required', False):
            self.fail('required')
        return super()._validate_missing(value)
    
    def serialize(self, attr, obj, accessor=None):
        if obj is not None and not isinstance(obj, list) and attr not in obj.__dict__:
            foreign_key_name = None
            if hasattr(obj, attr + '_id'):
                foreign_key_name = attr + '_id'
            elif hasattr(obj, 'id_' + attr):
                foreign_key_name = 'id_' + attr
            if foreign_key_name:
                value = getattr(obj, foreign_key_name)
                if value:
                    return {'id': int(value)}
        return super(SmartNested, self).serialize(attr, obj, accessor)
