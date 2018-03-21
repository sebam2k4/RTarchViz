# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post

class PostAdmin(admin.ModelAdmin):
  list_display = ("title", "author", "published_date", "updated_date", "status", "category")
  list_filter = ("status", "category", "created_date", "published_date", "updated_date")
  search_fields = ("title", "author")
  date_hierarchy = "published_date"
  ordering = ["status", "-published_date"]
  readonly_fields=("created_date", "published_date", "updated_date", "views_count", "slug",)
# Register your models here.
admin.site.register(Post, PostAdmin)