# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone


class Product(models.Model):
  """
  Defining Product's Post models
  """

  # CHOICES:
  CATEGORY_CHOICES = (
    ('assets', 'Assets'),
    ('environment', 'Environment'),
    ('blueprint', 'Blueprint'),
    ('materials', 'Materials')
  )
  NEWEST_VERSION = 419
  BASE_VERSION = 400
  UE_VERSION_CHOICES = [((str(i/100.00)),str(i/100.00)) for i in range(BASE_VERSION, BASE_VERSION + (NEWEST_VERSION - BASE_VERSION + 1))]


  # DATABASE FIELDS:
  seller = models.ForeignKey(settings.AUTH_USER_MODEL)
  name = models.CharField('Product Name', max_length=254, null=False)
  description = models.TextField(max_length=2000)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  sold_count = models.IntegerField('sold', editable=False, default=0)
  view_count = models.IntegerField('views', editable=False, default=0)
  added_date = models.DateTimeField(editable=False, default=timezone.now)
  category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
  ue_version = models.CharField('Unreal Engine Version', max_length=5, choices=UE_VERSION_CHOICES)
  main_image = models.ImageField(upload_to='product-images', blank=True, null=True)
  file_path = models.CharField(max_length=254, blank=True, null=True)
  def __unicode__(self):
    return self.name