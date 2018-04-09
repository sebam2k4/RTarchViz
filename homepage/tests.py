# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.contrib.auth import get_user_model
from blog.models import Post
# Create your tests here.

class HomePageTests(TestCase):

  def test_homepage(self):
    response = self.client.get('/')
    self.assertEqual(response.status_code, 200)
