from __future__ import unicode_literals
import six
from importlib import import_module

from django.db import models

from .encoder import JsonDocEncoder
from .document import RelatedDocument
from .serializable import JsonDocument


class JsonRelatedManager(object):
    """
    Mapping item structure:
     0 - Class or string to me imported
     1 - url_resolve sting
    """

    def __init__(self, value, mapping):
        self.value = value
        self.mapping = mapping
        self._cached_imports = {}

    def __str__(self):
        return str(self.value)

    def __getitem__(self, key):
        for item in self.value:
            if item['key'] == key:
                return RelatedDocument(self, item)
        raise KeyError

    def __len__(self):
        return len(self.value)

    def __iter__(self):
        for item in self.value:
            yield RelatedDocument(self, item)

    def get(self, key, default=None):
        """
        Return first occur of object
        :param key:
        :return:
        """
        try:
            return self[key]
        except KeyError:
            return default

    def get_list(self, key):
        rc = []
        for item in self.value:
            if item['key'] == key:
                rc.append(RelatedDocument(self, item))
        return rc

    def cls_resolve(self, key):
        """
        Return class by key
        :param key:
        :return:
        """
        cls_ref = self.mapping[key][0]
        if isinstance(cls_ref, six.string_types):
            if cls_ref not in self._cached_imports:
                module_path = cls_ref.split('.')
                module = import_module('.'.join(module_path[:-1]))
                self._cached_imports[cls_ref] = getattr(module, module_path[-1])
            return self._cached_imports[cls_ref]
        return cls_ref

    def url_resolve(self, key):
        try:
            return self.mapping[key][1]
        except IndexError:
            return None

    @staticmethod
    def _prepare(value):
        if isinstance(value, (models.Model, JsonDocument)):
            enc = JsonDocEncoder(value)
            return enc.dump()
        return value

    def append(self, obj):
        """
        :param obj: either dict or django.db.models.Model instance
        :return:
        """
        self.value.append(self._prepare(obj))

    def extend(self, objects):
        for item in objects:
            self.append(item)

    def insert(self, pos, obj):
        self.value.insert(pos, self._prepare(obj))

    def remove(self, obj):
        value = self._prepare(obj)
        for item in self.value:
            if item['key'] == value['key'] and item['pk'] == value['pk']:
                self.value.remove(item)
                break

    def clear(self):
        self.value = list()
