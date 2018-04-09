# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product, Review

class ProductAdmin(admin.ModelAdmin):
  readonly_fields = ('view_count', 'sold_count', 'added_date')
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Review)
