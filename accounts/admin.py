# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import User

# Register your models here.

class AccountsUserAdmin(admin.ModelAdmin):

    list_display = (
        "email", "username", "last_login",
        "first_name", "last_name", "is_staff"
    )
    list_filter = ("is_staff", "is_superuser")
    search_fields = ("email", "username", "first_name", "last_name")
    ordering = ('-last_login',)

admin.site.register(User, AccountsUserAdmin)