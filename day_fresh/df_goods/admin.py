# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
import models
# Register your models here.

class GoodsInfoLine(admin.TabularInline):
    model = models.GoodsInfo

class TypeInfoAdmin(admin.ModelAdmin):
    inlines = [GoodsInfoLine]


admin.site.register(models.TypeInfo,TypeInfoAdmin)
admin.site.register(models.GoodsInfo)
