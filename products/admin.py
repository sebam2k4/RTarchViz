# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Product, Review

class ReviewAdmin(admin.ModelAdmin):
  list_display = ("product", "rating", "review_text", "added_date", "buyer",)


class ProductAdmin(admin.ModelAdmin):
  list_display = ("name", "added_date", "seller", "price", "view_count", "sold_count")
  list_filter = ("seller", "view_count", "sold_count")
  ordering = ["-sold_count"]
  
  readonly_fields = ('view_count', 'added_date')
# Register your models here.
admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
