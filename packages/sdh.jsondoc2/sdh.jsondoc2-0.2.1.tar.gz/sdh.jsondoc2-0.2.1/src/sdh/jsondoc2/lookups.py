from psycopg2.extras import Json

from django.db.models import Lookup, Model
from .encoder import JsonDocEncoder


class ContainsModel(Lookup):
    lookup_name = 'has_object'
    prepare_rhs = False

    def process_rhs(self, compiler, connection):
        value = self.rhs
        if isinstance(value, Model):
            lookup_key = JsonDocEncoder(value).key()
            return ('%s', [Json([lookup_key])])
        return super(ContainsModel, self).process_rhs(compiler, connection)

    def as_sql(self, qn, connection):
        lhs, lhs_params = self.process_lhs(qn, connection)
        rhs, rhs_params = self.process_rhs(qn, connection)
        params = lhs_params + rhs_params
        return '%s @> %s' % (lhs, rhs), params
