# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from products.models import Product

# Create your models here.

class Order(models.Model):
  """ Defining Order models """

  # DATABASE FIELDS
  buyer = models.ForeignKey(settings.AUTH_USER_MODEL)
  ordered_date = models.DateTimeField(editable=False)
  product_count = models.IntegerField(editable=False, blank=False, null=False)
  total_amount = models.DecimalField(editable=False, max_digits=8, decimal_places=2)
  products = models.ManyToManyField(Product, through='OrderProduct', related_name='ordered_products')

  # TO STRING METHOD
  def __unicode__(self):
    return "Order #{0}, {1} ----- Order made by: {2}".format(self.id, self.ordered_date, self.buyer.username)

  # MODEL METHODS
  def order_total(self):
    return '€{0}'.format(self.total_amount)


# Intermediate model for m-m relationship between Order and Product
class OrderProduct(models.Model):
  """ Defining Order Product models """

  # DATABASE FIELDS
  order = models.ForeignKey(Order, null=False)
  product = models.ForeignKey(Product, null=False)

  # TO STRING METHOD
  def __unicode__(self):
    return "{0} by {1} {2} ---- purchased by {3}".format(self.product.name, self.product.seller.username, self.product.price, self.order.buyer.username)