# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from products.models import Product
from django.utils import timezone

class OrderManager(models.Manager):
  """ define custom manager """

  def purchased_products(self, user):
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

  # MANAGERS
  objects = OrderManager()

  # TO STRING METHOD
  def __unicode__(self):
    return "Order #{0}".format(self.id)

  # MODEL METHODS
  def order_total(self):
    return '€{0}'.format(self.total_amount)


# Intermediate model for m-m relationship between Order and Product
class OrderProduct(models.Model):
  """ 
  Defining Order Product models
  (Intermediate Table for Order-Product relationship)
  """

  # DATABASE FIELDS
  order = models.ForeignKey(Order, null=False)
  product = models.ForeignKey(Product, null=False)

  # TO STRING METHOD
  def __unicode__(self):
    return "{0} from (Order #{1}) - seller: {2}".format(self.product.name, self.order_id, self.product.seller.username)


class PurchaseHistoryManager(models.Manager):
  """ define custom manager """

  def purchased_products_history(self, user):
    """ get user's purchased products """
    return self.get_queryset().filter(buyer_id=user.id).order_by('-purchase_date')

  def sold_products_history(self, user):
    """ get user's sold products """
    return self.get_queryset().filter(seller_id=user.id).order_by('-purchase_date')


class PurchaseHistory(models.Model):
  """
  Purchases History for recording transactional details for each product
  item at time of purchase. This keeps transaction history accurate as
  it may otherwise change when user updates product price, name or
  removes product. Used for dashboard analytics.
  """
  # DATABASE FIELDS
  product_price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
  product_name = models.CharField(max_length=200)
  purchase_date = models.DateTimeField(default=timezone.now)
  product = models.ForeignKey(Product, null=False)
  buyer_id = models.IntegerField(blank=False, null=False)
  seller_id = models.IntegerField(blank=False, null=False)
  order = models.ForeignKey(Order, null=False)

  # MANAGERS:
  objects = PurchaseHistoryManager()

  # TO STRING METHOD
  def __unicode__(self):
    return '{0} €{1}'.format(self.product_name, self.product_price)