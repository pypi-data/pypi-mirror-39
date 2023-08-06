# -*- coding:utf-8 -*-

import six
from django.contrib import admin
from knob.admin import rich_tag
import json
from .models import *


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'klass_', 'init_arg', 'generator']
    search_fields = ['name', 'klass_path']

    def klass_(self, obj):
        if not obj.klass_path:
            text = "No Klass"
            color = "gray"
        else:
            try:
                klass = obj.klass
                text = obj.klass_path
                color = "green"
            except Exception as e:
                text = repr(e)
                color = 'red'
        return rich_tag(text, color=color, bold=True)
    klass_.allow_tags = True


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ['category', 'name', 'active', 'para_']
    list_filter = ['active', 'category']
    search_fields = ['name']
    actions = ['activate', 'deactivate', 'toggle_active']

    def para_(self, obj):
        compact_json = json.dumps(obj.para)[:80]
        full_json = json.dumps(obj.para, indent=2)
        return rich_tag(text=compact_json, hint=full_json)
    para_.allow_tags = True

    def activate(self, request, queryset):
        for item in queryset.all():
            try:
                item.active = True
                item.save()
            except Exception as e:
                six.print_(e)

    def deactivate(self, request, queryset):
        for item in queryset.all():
            try:
                item.active = False
                item.save()
            except Exception as e:
                six.print_(e)

    def toggle_active(self, request, queryset):
        for item in queryset.all():
            try:
                item.active = not item.active
                item.save()
            except Exception as e:
                six.print_(e)
