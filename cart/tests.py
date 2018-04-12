# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from products.models import Product


class CartViewTest(TestCase):
  """ Tests for Cart View """
  def test_view_url_exists_at_desired_location(self):
    response = self.client.get('/cart/')
    self.assertEqual(response.status_code, 200)

  def test_view_url_accessible_by_name(self):
    response = self.client.get(reverse('view_cart'))
    self.assertEqual(response.status_code, 200)
  
  def test_view_uses_correct_template(self):
    response = self.client.get(reverse('view_cart'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'base.html')
    self.assertTemplateUsed(response, 'cart.html')
      

class AddToCartViewTest(TestCase):
  """ Tests for add to cart view """

  def setUp(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    self.product = Product.objects.create(seller=self.user, name='product-1', description='description-1', ue_version='4.18', price=10, category='assets')

  # def test_view_url_exists_at_desired_location(self):
  #   # not working
  #   response = self.client.get('/cart/add/1')
  #   self.assertEqual(response.status_code, 200)

  # def test_view_url_accessible_by_name(self):
  #   response = self.client.get(reverse('add_to_cart', kwargs={'product_id': self.product.id}))
  #   self.assertEqual(response.status_code, 200)
