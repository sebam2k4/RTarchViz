# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, OrderProduct, PurchaseHistory


class PurchaseHistoryAdmin(admin.ModelAdmin):
    """ Custom Admin for Purchase History """
    list_display = ("product", "product_price", "get_seller",
                    "order", "purchase_date", "get_buyer")
    search_fields = ("product", )
    list_filter = ("purchase_date",)

    def get_seller(self, obj):
        """ get seller from foreign field """
        return obj.product.seller.username
        
    # make foreign field sortable and define its column name
    get_seller.admin_order_field = 'product__seller'
    get_seller.short_description = 'seller'

    def get_buyer(self, obj):
        """ get buyer from foreign field """
        return obj.order.buyer.username

    # make foreign field sortable and define its column name
    get_buyer.admin_order_field = 'order__buyer'
    get_buyer.short_description = 'buyer'


class OrderProductAdminInline(admin.TabularInline):
    fields = ('product',)
    model = OrderProduct
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    """ custom admin for managing Orders """
    list_display = ("__unicode__", "ordered_date",
                    "product_count", "buyer", "order_total",)
    list_filter = ("ordered_date",)
    inlines = (OrderProductAdminInline, )
    exclude = ('products',)
    readonly_fields = ('ordered_date', 'product_count', 'order_total')


admin.site.register(Order, OrderAdmin)
admin.site.register(OrderProduct)
admin.site.register(PurchaseHistory, PurchaseHistoryAdmin)
