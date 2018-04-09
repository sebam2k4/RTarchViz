# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.text import slugify


class PostModelTest(TestCase):
  """ Tests for Post Model """
  def test_string_representation(self):
    post = Post(title="My blog post title")
    self.assertEqual(str(post), post.title)

  def test_get_absolute_url(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    post = Post.objects.create(title='1-title', content='1-content', published_date=timezone.now(), slug='1-title', author=self.user)
    self.assertIsNotNone(post.get_absolute_url())


class BlogPostListViewTest(TestCase):
  """ Tests for Blog Post List view """
  def test_blog_list_page(self):
    response = self.client.get('/blog/')
    self.assertEqual(response.status_code, 200)

  """Test whether blog posts show up on the Blog list view"""

  def setUp(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')

  def test_one_published_post(self):
    Post.objects.create(title='1-title', content='1-content', author=self.user, status='published')
    response = self.client.get('/blog/')
    self.assertContains(response, '1-title')
    self.assertContains(response, '1-content')

  def test_one_draft_post(self):
    Post.objects.create(title='2-title', content='2-content', author=self.user, status='draft')
    response = self.client.get('/blog/')
    self.assertNotContains(response, '2-title')
    self.assertNotContains(response, '2-content')

  def test_two_published_posts(self):
    Post.objects.create(title='3-title', content='3-content', author=self.user, status='published')
    Post.objects.create(title='4-title', content='4-content', author=self.user, status='published')
    response = self.client.get('/blog/')
    self.assertContains(response, '3-title')
    self.assertContains(response, '3-content')
    self.assertContains(response, '4-title')
    self.assertContains(response, '4-content')

  def test_one_published_and_one_draft_posts(self):
    Post.objects.create(title='5-title', content='5-content', author=self.user, status='published')
    Post.objects.create(title='6-title', content='6-content', author=self.user, status='draft')
    response = self.client.get('/blog/')
    self.assertContains(response, '5-title')
    self.assertContains(response, '5-content')
    self.assertNotContains(response, '6-title')
    self.assertNotContains(response, '6-content')


class BlogPostDetailViewTest(TestCase):
  """ Tests for Blog Post Detail view """
  def setUp(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    self.post = Post.objects.create(title='1-title', content='1-content', published_date=timezone.now(), slug='1-title', author=self.user)

  def test_detail_view(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertEqual(response.status_code, 200)

  def test_title_in_post(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertContains(response, self.post.title)

  def test_content_in_post(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertContains(response, self.post.content)