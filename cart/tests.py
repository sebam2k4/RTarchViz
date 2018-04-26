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
