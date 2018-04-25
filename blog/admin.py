# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.db import models
from .models import Post, PostViewCount
from django.contrib.auth import get_user_model
from django.utils.translation import gettext, gettext_lazy as _
from tinymce.widgets import TinyMCE


class PostViewCountInline(admin.TabularInline):
    model = PostViewCount


class PostAdmin(admin.ModelAdmin):
    """
    custom admin for managing Blog Posts
    """
    list_display = ("title", "author", "get_short_content", "published_date",
                    "updated_date", "status", "category", "get_view_count",)

    list_filter = ("status", "category", "created_date",
                   "published_date", "updated_date")
    search_fields = ("title", "author")
    date_hierarchy = "published_date"
    ordering = ["status", "-published_date"]

    readonly_fields = ("created_date", "published_date",
                       "updated_date", "slug",)
    fieldsets = (
        (None, {'fields': ('author', 'title', 'slug', 'content', 'category')}),
        (_('Image'), {'fields': ('image',)}),
        (_('Status'), {'fields': ('status',)}),
        (_('History'), {'fields': ('created_date', 'published_date',
                                   'updated_date')}),
    )

    # override all textfields to use the tinyMCE widget
    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()},
    }

    inlines = (PostViewCountInline,)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        override default formfield for a foreign key field (author) to
        return only users who are staff
        """
        if db_field.name == 'author':
            kwargs['queryset'] = get_user_model().objects.filter(
                is_staff=request.user.is_staff)

        return super(PostAdmin, self).formfield_for_foreignkey(
            db_field, request, **kwargs)

    def get_view_count(self, obj):
        """
        get view count from related one-to-one field 
        and make the field sortable
        """
        return obj.postviewcount.view_count

    # get view count from model OneToOneField and make it order-able
    get_view_count.admin_order_field = 'postviewcount__view_count'
    get_view_count.short_description = 'view count'


admin.site.register(Post, PostAdmin)
# admin.site.register(PostViewCount)
