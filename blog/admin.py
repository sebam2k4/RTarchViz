# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Post
from django.utils.translation import gettext, gettext_lazy as _

class PostAdmin(admin.ModelAdmin):
  list_display = ("title", "author", "published_date", "updated_date", "status", "category", "views_count")
  list_filter = ("status", "category", "created_date", "published_date", "updated_date")
  search_fields = ("title", "author")
  date_hierarchy = "published_date"
  ordering = ["status", "-published_date"]

  readonly_fields=("created_date", "published_date", "updated_date", "views_count", "slug",)
  fieldsets = (
                (None,          {'fields': ('title', 'slug', 'content', 'category')}),
                (_('Status'),   {'fields': ('status',)}),
                (_('History'),  {'fields': ('created_date', 'published_date', 'updated_date')}),
                (_('Views'),  {'fields': ('views_count',)}),
              )
    
# Register your models here.
admin.site.register(Post, PostAdmin)