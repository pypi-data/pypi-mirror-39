# -*- coding:utf-8 -*-

import six
from django.db import models
from easy_jsonfield import JSONField
from krux.functools.cache import cache
from krux.converters import str2obj


@six.python_2_unicode_compatible
class Category(models.Model):
    class Meta:
        pass

    name = models.CharField(max_length=64, primary_key=True)
    klass_path = models.CharField(max_length=255, default='', null=True, blank=True)
    init_arg = models.CharField(max_length=64, null=True, blank=True)
    generator = models.CharField(max_length=64, null=True, blank=True)

    def __str__(self):
        return self.name

    @property
    def klass(self):
        if not self.klass_path:
            return None
        return str2obj(self.klass_path)

    def get(self, key, *args):
        if isinstance(key, six.string_types):
            para = self.items.get(name=key).para
            para = para.copy()
            para.setdefault('name', key)
        elif isinstance(key, dict):
            para = key.copy()
        else:
            raise KeyError(u'Not a valid key for KonfCategory {}: {}'.format(self.name, key))

        if self.klass is None:
            return para

        if not self.init_arg:
            obj = self.klass(**para)
        else:
            obj = self.klass(**{self.init_arg: para})

        if not self.generator:
            return obj
        else:
            return getattr(obj, self.generator)(*args)

    def get_all(self):
        results = []
        for item in self.items.filter(active=True):
            try:
                results.append(self.get(item.para))
            except Exception as e:
                pass
        return results


@six.python_2_unicode_compatible
class Item(models.Model):
    class Meta:
        unique_together = [('category', 'name')]

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=128)
    para = JSONField(default=dict, null=True, blank=True)

    active = models.BooleanField(default=True)

    def __str__(self):
        return u"{}/{}".format(self.category.name, self.name)

    def to_json(self):
        result = {
            "type": "KonfItem",
            "category": self.category.name,
            "name": self.name,
            "para": self.para
        }
        return result
