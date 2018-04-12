# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
import os
from django.core.exceptions import ValidationError


def user_directory_path(instance, filename):
  """
  product main images and file will be uploaded to
  MEDIA_ROOT/seller_id_<id>/product_name_<slug>-<filename>
  note: see if can incorporate username in addition to seller_id
  (need to import User model?)
  * cannot use instance.id as the instance has not yet been saved
  at this point. id is generated incrementally by db.
  * Need to make a check if user changed product title to update
  file name accordingly (maybe in save method)
  """
  return 'products/seller_id_{0}/product_name_{1}-{2}'.format(instance.seller_id,
                                                              instance.slug, filename)

def validate_file_extension(file):
    if not file.name.endswith('.zip'):
      raise ValidationError('Only single .zip file is allowed')


class Product(models.Model):
  """
  Defining Product models
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
  # version choices as floats converted to string (4.19, 4.18, etc.)
  UE_VERSION_CHOICES = [(str(i/100.00),str(i/100.00)) for i in range(NEWEST_VERSION, BASE_VERSION -1, -1)]

  # DATABASE FIELDS:
  seller = models.ForeignKey(settings.AUTH_USER_MODEL)
  name = models.CharField('Product Name', max_length=254, null=False)
  slug = models.SlugField(editable=False, max_length=254)
  description = models.TextField(max_length=2000)
  price = models.DecimalField(max_digits=6, decimal_places=2)
  sold_count = models.IntegerField('sold', editable=False, default=0)
  view_count = models.IntegerField('views', editable=False, default=0)
  added_date = models.DateTimeField(editable=False, default=timezone.now)
  category = models.CharField(max_length=25, choices=CATEGORY_CHOICES)
  ue_version = models.CharField('Unreal Engine Version', max_length=5,
                                choices=UE_VERSION_CHOICES, default=UE_VERSION_CHOICES[0])
  main_image = models.ImageField('Main Product Image', upload_to=user_directory_path,
                                 blank=True, null=True)
  product_file = models.FileField('Product File', upload_to=user_directory_path, null=False,
                                  validators=[validate_file_extension])
 
  # META CLASS:
  class Meta:
    """specify global meta options for model"""
    ordering = ('-added_date',) # set default ordering of the objects

  # TO STRING METHOD:
  def __unicode__(self):
    return self.name
    
  # SAVE METHOD:
  def save(self, *args, **kwargs):
    """
    overwrite Model save method to automatically generate a slug
    from product;s name
    """
    self.slug = slugify(self.name)
    # detect if title has changed
    if self.pk is not None:
      original = Product.objects.get(pk=self.pk)
      if original.name != self.name:
        # rename product filename to reflect new product name
        new_file_name = 'products/seller_id_{0}/product_name_{1}.zip'.format(str(self.seller_id), str(self.slug))
        os.rename('./media/{0}'.format(str(self.product_file)), './media/{0}'.format(new_file_name))
        self.product_file = new_file_name
    super(Product, self).save(*args, **kwargs)

  # ABSOLUTE URL METHODS:
  def get_absolute_url(self):
    return reverse('product_detail', args=[self.slug, self.id])

  def get_edit_product_url(self):
    return reverse('edit_product', args=[self.slug, self.id])

  def get_delete_product_url(self):
    return reverse('delete_product', args=[self.slug, self.id])

  # MODEL METHODS
  def euro_price(self):
    return '€{0}'.format(self.price)

  
        
class Review(models.Model):
  """
  Defining product review models
  """
  
  # CHOICES
  # Restrict rating to choices 1 thru 5
  RATING_CHOICES = [(i, i) for i in range(1, 6)]
  
  # DATABASE FIELDS:
  buyer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reviews')
  product = models.ForeignKey(Product, related_name='reviews')
  rating = models.IntegerField(choices=RATING_CHOICES, null=False)
  review_text = models.TextField(max_length=700, blank=True, null=True)
  added_date = models.DateTimeField(editable=False, default=timezone.now)
  
  # META CLASS:
  class Meta:
    """specify global meta options for model"""
    ordering = ('-added_date',) # set default ordering of the objects

  # TO STRING METHOD:
  def __unicode__(self):
    return '{0} review by {1}'.format(self.product.name, self.buyer.username)

  # ABSOLUTE URL METHODS:
  def get_edit_review_url(self):
    return reverse('edit_review', args=[self.product.slug, self.product.id, self.id])

  def get_delete_review_url(self):
    return reverse('delete_review', args=[self.product.slug, self.product.id, self.id])