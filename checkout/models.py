# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from products.models import Product
from django.utils import timezone

class OrderManager(models.Manager):
  """ define custom manager """

  def owned_products(self, user):
    """ get user's purchased products """
    orders = self.get_queryset().filter(buyer_id=user.id)
    owned_assets = []
    for order in orders:
      for item in order.products.all():
        owned_assets.append(item)
    return owned_assets


class Order(models.Model):
  """ Defining Order models """

  # DATABASE FIELDS
  buyer = models.ForeignKey(settings.AUTH_USER_MODEL)
  ordered_date = models.DateTimeField(editable=False, default=timezone.now)
  product_count = models.IntegerField(editable=False, blank=False, null=False, default=0)
  total_amount = models.DecimalField(editable=False, max_digits=8, decimal_places=2, default=0.00)
  products = models.ManyToManyField(Product, through='OrderProduct', related_name='ordered_products')

  # MANAGERS:
  objects = OrderManager()
  #objects = models.Manager()

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


class PurchaseHistory(models.Model):
  """
  Purchases History for recording transactional details for each product
  item at time of purchase. This keeps transaction history accurate as
  it may otherwise change when user updates product price or removes
  product. Used for dashboard analytics. Also, this table makes sure
  that the digital project is still available to user who purchased it
  even though the seller has deleted the product from the market.
  """
  # DATABASE FIELDS
  product_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  product_name = models.CharField(max_length=200)
  purchase_date = models.DateTimeField(default=timezone.now)
  product = models.ForeignKey(Product, null=False)
  buyer_id = models.IntegerField(blank=False, null=False)
  seller_id = models.IntegerField(blank=False, null=False)
  order = models.ForeignKey(Order, null=False)
  product_file = models.FileField()

