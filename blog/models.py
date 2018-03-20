# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings

# Create your models here.

class Post(models.Model):
  """
  Defining Blog's Post models
  """
  # author is linked to a registered staff user, via the User model in the accounts app.
  author = models.ForeignKey(settings.AUTH_USER_MODEL)
  title = models.CharField(max_length=200)
  # slug is generated from the title
  slug = models.SlugField(editable=False, max_length=200, unique=True)
  content = models.TextField()
  # identify when post was created
  created_date = models.DateTimeField(editable=False, default=timezone.now)
  # set publish date initially to blank and null as drafts are allowed
  # published date will be set once post is published
  published_date = models.DateTimeField(editable=False, blank=True, null=True)
  # record when a published post is last edited
  updated_date = models.DateTimeField(editable=False, blank=True, null=True)
  # record how often a post is seen
  views_count = models.IntegerField(editable=False, default=0)
  # blog post's category
  CATEGORY_CHOICES = (
    ('news', 'News'),
    ('tutorial', 'Tutorial')
  )
  category = models.CharField(max_length=10, choices=CATEGORY_CHOICES, default='news')
  # blog post's status
  STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published')
  )
  status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

  def __str__(self):
    """ identify blog entries by their title for admin page """
    return self.title