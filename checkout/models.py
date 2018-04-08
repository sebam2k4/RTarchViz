# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):
  buyer = models.ForeignKey(settings.AUTH_USER_MODEL)
  ordered_date = models.DateTimeField()
  product_count = models.IntegerField(blank=False, null=False)
  total_amount = models.DecimalField(max_digits=8, decimal_places=2)
  products = models.ManyToManyField(Product, through='OrderProduct', related_name='ordered_products')

  def __str__(self):
    return "Order #{0}, {1} ----- Order made by: {2}".format(self.id, self.ordered_date, self.buyer.username)

# Intermediate model for m-m relationship between Order and Product
class OrderProduct(models.Model):
  """
  Define Product line 
  """
  order = models.ForeignKey(Order, null=False)
  product = models.ForeignKey(Product, null=False)

  def __str__(self):
    return "{0} by {1} {2} ---- purchased by {3}".format(self.product.name, self.product.seller.username, self.product.price, self.order.buyer.username)