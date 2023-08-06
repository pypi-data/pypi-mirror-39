# -*- coding:utf-8 -*-

import six
import os
import json

from krux.types import Singleton
from krux.converters import parse_bool
from krux.functools.cache import cache
from krust.pather import *

__all__ = ['KonfCategory', 'Konfluence', 'konfer']


class KonfCategory(object):
    def __init__(self, name, klass=None, init_arg=None, generator=None, konfer=None):
        self.name = name
        self.klass = klass
        self.init_arg = init_arg
        self.generator = generator
        self.konfer = konfer

    def get(self, key, *args):
        if isinstance(key, six.string_types):
            para = self.load_item(key)
        elif isinstance(key, dict):
            if self.klass is None:
                return key
            para = key
        else:
            raise KeyError(u'Not a valid key for KonfCategory {}: {}'.format(self.name, repr(key)))

        if not self.init_arg:
            obj = self.klass(**para)
        else:
            obj = self.klass(**{self.init_arg: para})

        if not self.generator:
            return obj
        else:
            return getattr(obj, self.generator)(*args)

    def load_item(self, key):
        item_name = os.path.join(self.name, key)
        item_path = self.konfer.pather[item_name]

        with open(item_path) as f:
            # TODO: jsmin
            return json.load(f, strict=False)


class Konfluence(Singleton):
    _inited = False

    def __init__(self):
        if not self._inited:
            self.use_django = parse_bool(os.getenv('KONFLUENCE_USE_DJANGO', False))
            if not os.getenv('KONFLUENCE_PATH'):
                self.pather = Pather(paths=['/etc/konfluence', '~/.konfluence', './konf'])
            else:
                self.pather = Pather(env_var='KONFLUENCE_PATH')
            self.categories = {}
            self._inited = True

    @property
    @cache
    def DJCategory(self):
        # delay importing Category, to prevent recursive dependency.
        from .models import Category
        return Category

    def register(self, name, klass=None, init_arg=None, generator=None):
        self.categories[name] = KonfCategory(name,
                                             klass=klass, init_arg=init_arg, generator=generator,
                                             konfer=self)

    def __getitem__(self, key):
        catname, sub = key.split('/', 1)
        return self._get_from_category(catname, sub)

    def get(self, key, default=None):
        try:
            return self.__getitem__(key)
        except KeyError:
            pass

        if default is None:
            return default
        elif isinstance(default, six.string_types) and '/' in default:
            # 针对default是一个含有catname部分的key的情形
            return self.__getitem__(default)
        else:
            # default是字典, 或不含catname的key等.
            catname, sub = key.split('/', 1)
            return self._get_from_category(catname, default)

    def _get_from_category(self, category, key):
        if self.use_django:
            category = self._ensure_dj_category(category)
        else:
            category = self._ensure_fs_category(category)

        if isinstance(key, six.string_types):
            if key == '*':
                return category.get_all()
            else:
                tks = key.split(':')
                return category.get(*tks)
        elif isinstance(key, dict):
            return category.get(key)
        else:
            return key

    def _ensure_dj_category(self, category):
        if isinstance(category, six.string_types):
            category = self.DJCategory.objects.get(name=category)
        return category

    def _ensure_fs_category(self, category):
        if not isinstance(category, KonfCategory):
            category = self.categories[category]
        return category


konfer = Konfluence()