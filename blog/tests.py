# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Post
from django.contrib.auth import get_user_model
from django.urls import reverse


class PostModelTest(TestCase):
  """ Tests for Post Model """
  def test_string_representation(self):
    post = Post(title="My blog post title")
    self.assertEqual(str(post), post.title)

  def test_get_absolute_url(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    post = Post.objects.create(title='1-title', content='1-content', status='published', slug='1-title', author=self.user)
    self.assertIsNotNone(post.get_absolute_url())

  def test_get_author_name_method(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com', first_name='John', last_name='Wick')
    post = Post.objects.create(title='1-title', content='1-content', status='published', author=self.user)
    full_name = post.get_author()
    self.assertEqual(full_name, 'John Wick')

  def test_get_author_method_when_no_name(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    post = Post.objects.create(title='1-title', content='1-content', status='published', author=self.user)
    full_name = post.get_author()
    self.assertEqual(full_name, self.user.username)

  def test_post_published_date(self):
    # setting 'published' status should record a published_date timestamp
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    post = Post.objects.create(title='1-title', content='1-content', status='published', author=self.user)
    self.assertIsNotNone(post.published_date)
    self.assertIsNone(post.updated_date)

  def test_post_updated_date(self):
    """ updating a post should record updated_date timestamp """
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    post = Post.objects.create(title='1-title', content='1-content', status='published', author=self.user)
    post.content = 'updated content'
    post.save()
    self.assertIsNotNone(post.updated_date)


class BlogPostListViewTest(TestCase):
  """ Tests for Blog Post List view """
  def test_view_url_exists_at_desired_location(self):
    response = self.client.get('/blog/')
    self.assertEqual(response.status_code, 200)

  def test_view_url_accessible_by_name(self):
    response = self.client.get(reverse('posts_list'))
    self.assertEqual(response.status_code, 200)

  #Test whether blog posts show up on the Blog list view:

  def setUp(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')

# make assertion that doesn't exist first
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

  # test pagination for Blog list view:

  @classmethod
  def setUpTestData(cls):
    #Create 11 posts for pagination tests
    author = get_user_model().objects.create(username='author1', email='author1@gmail.com')
    number_of_posts = 11
    for post_num in range(number_of_posts):
      Post.objects.create(author=author, title='title {0}'.format(post_num), content='content {0}'.format(post_num), status='published')

  def test_pagination_is_4(self):
    response = self.client.get(reverse('posts_list'))
    self.assertEqual(response.status_code, 200)
    # Confirm page has exactly 4 posts
    self.assertEqual( len(response.context['posts']), 4)

  def test_lists_all_posts(self):
    """ Get third page and confirm it has exactly 3 posts remaining """
    response = self.client.get(reverse('posts_list')+'?page=3')
    self.assertEqual(response.status_code, 200, "Return code must be 200")
    self.assertEqual( len(response.context['posts']), 3)

  def test_show_last_page_when_requesting_out_of_range(self):
    """ Get third page and confirm it has exactly 3 posts remaining """
    response = self.client.get(reverse('posts_list')+'?page=50')
    self.assertEqual(response.status_code, 200)
    self.assertEqual( len(response.context['posts']), 3)


class BlogPostDetailViewTest(TestCase):
  """ Tests for Blog Post Detail view """
  def setUp(self):
    self.user = get_user_model().objects.create(username='test_user', email='test_user@gmail.com')
    self.post = Post.objects.create(title='1-title', content='1-content', status='published', slug='1-title', author=self.user)

  def test_view_url_exists_at_desired_location(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertEqual(response.status_code, 200)

  def test_title_in_post(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertContains(response, self.post.title)

  def test_content_in_post(self):
    response = self.client.get(self.post.get_absolute_url())
    self.assertContains(response, self.post.content)

