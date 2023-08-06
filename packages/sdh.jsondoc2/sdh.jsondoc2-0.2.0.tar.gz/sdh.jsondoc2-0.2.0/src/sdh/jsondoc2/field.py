from __future__ import print_function, unicode_literals
from psycopg2.extras import Json
from django.contrib.postgres.fields import JSONField

from .manager import JsonRelatedManager
from . import lookups


class RelatedDocField(JSONField):
    def __init__(self, mapping={}, **kwargs):
        self.mapping = mapping
        super(RelatedDocField, self).__init__(**kwargs)

    def from_db_value(self, value, expression, connection, context):
        return JsonRelatedManager(value, self.mapping)

    def get_default(self):
        return JsonRelatedManager(list(), self.mapping)

    def get_prep_value(self, value):
        if value is not None:
            if isinstance(value, list):
                return Json(value)
            return super(RelatedDocField, self).get_prep_value(value.value)
        return value


RelatedDocField.register_lookup(lookups.ContainsModel)
