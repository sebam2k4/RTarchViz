# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from .models import Post
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from tinymce.widgets import TinyMCE

class PostAdmin(admin.ModelAdmin):
  """
  custom admin
  """
  list_display = ("title", "author", "published_date", "updated_date", "status", "category",
                  "view_count")
  list_filter = ("status", "category", "created_date", "published_date", "updated_date")
  search_fields = ("title", "author")
  date_hierarchy = "published_date"
  ordering = ["status", "-published_date"]

  readonly_fields=("created_date", "published_date", "updated_date",
                   "view_count", "slug",)
  fieldsets = (
    (None,         {'fields': ('author',  'title', 'slug', 'content', 'category')}),
    (_('Image'),   {'fields': ('image',)}),
    (_('Status'),  {'fields': ('status',)}),
    (_('History'), {'fields': ('created_date', 'published_date', 'updated_date')}),
    (_('Views'),   {'fields': ('view_count',)}),
  )

  # override all textfields to use the tinyMCE widget
  formfield_overrides = {
    models.TextField: {'widget': TinyMCE()},
  }

  def formfield_for_foreignkey(self, db_field, request, **kwargs):
    """
    override default formfield for a foreign key field (author) to
    return only users who are staff
    """
    if db_field.name == 'author':
      # use get_user_model to return current active user model instead
      # of 'import accounts.User'
      kwargs['queryset'] = get_user_model().objects.filter(is_staff=request.user.is_staff)
    return super(PostAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

# Register your models here.
admin.site.register(Post, PostAdmin)