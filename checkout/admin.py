# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderProduct
from django.utils.translation import gettext, gettext_lazy as _
  
class OrderProductAdminInline(admin.TabularInline):
  fields = ('product',)
  model = OrderProduct
  extra = 0
  

class OrderAdmin(admin.ModelAdmin):
  inlines = (OrderProductAdminInline, )
  exclude = ('products',)
  readonly_fields = ('ordered_date', 'product_count', 'order_total')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
