from __future__ import unicode_literals
from django.utils.encoding import python_2_unicode_compatible
from django.core.urlresolvers import reverse
from django.urls.exceptions import NoReverseMatch


@python_2_unicode_compatible
class RelatedDocument(object):
    """
    item element keys
     - key: Reference to correspondent structure in the
     - pk: PK of the object
     - label: (optional) extended label of the object
     - url_args: (optional) list of args to be assed into resolve, instead (pk,) will be used

    """

    def __init__(self, object_manager, item):
        self.object_manager = object_manager
        self.item = item

    def __str__(self):
        if 'label' in self.item:
            return "<%s=%s: %s>" % (self.key, self.pk, self.item['label'])
        return "<%s=%s>" % (self.key, self.pk)

    @property
    def key(self):
        return self.item['key']

    @property
    def pk(self):
        return self.item['pk']

    @property
    def label(self):
        try:
            return self.item['label']
        except KeyError:
            return "%s: %s" % (self.key, self.pk)

    @property
    def instance(self):
        """
        Return instance of the related object with database request
        :return:
        """
        cls = self.object_manager.cls_resolve(self.key)
        return cls.objects.get(pk=self.pk)

    @property
    def fake(self):
        """
        Return fake wrapped object with pk only without request database
        :return:
        """
        cls = self.object_manager.cls_resolve(self.key)
        return cls(pk=self.pk)

    @property
    def url(self):
        url_resolve = self.object_manager.url_resolve(self.key)
        if not url_resolve:
            return None
        url_args = self.item.get('url_args', [self.pk])
        return reverse(url_resolve, args=url_args)

    def get_url(self, default=None):
        try:
            return self.url
        except NoReverseMatch:
            return default
