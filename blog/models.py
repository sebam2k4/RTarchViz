# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import permalink

class PostManager(models.Manager):
  """
  Defining custom Manager methods
  """

  def published(self):
    """ select only published posts """
    return self.get_queryset().filter(status="published")

  # note: find a more elegant way get next/prev post objects
  #       for post_detail navigation
  def get_next_post(self, published_date):
    """
    get a queryset of post objects that were published after current
    post, arrange in ascending order, and then select the next post.
    Or select latest post when no next post available. (select current post)
    """
    try:
      return self.get_queryset().filter(published_date__gt=published_date).order_by('published_date')[:1][0]
    except IndexError:
      return self.get_queryset().latest('published_date')

  def get_prev_post(self, published_date):
    """
    get a queryset of post objects that were published before current
    post, arrange in descending order, and then select the next post.
    Or select oldest post when no previous post available. (select current post)
    """
    try:
      return self.get_queryset().filter(published_date__lt=published_date).order_by('-published_date')[:1][0]
    except IndexError:
      return self.get_queryset().earliest('published_date')

class Post(models.Model):
  """
  Defining Blog's Post models
  """
  # author is linked to a registered staff user, via the User model in the accounts app.
  author = models.ForeignKey(settings.AUTH_USER_MODEL)
  title = models.CharField(max_length=200, unique=True)
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
  view_count = models.IntegerField('views', editable=False, default=0)
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

  # add images to a post (stores relative path to image)
  image = models.ImageField(upload_to="images", blank=True, null=True)

  objects = PostManager()
  
  def get_slug(self):
    """
    create a slug from post's title
    """
    slug = slugify(self.title)
    return slug
 
  def save(self, *args, **kwargs):
    """
    overwrite Model save method to 
    1. automatically generate a slug from post's title
    2. set published_date with current date & time when post's status is initially
       changed from 'draft' to 'published'
    3. set updated_date with current date & time if published_date already set
    """
    self.slug = self.get_slug()
    if self.status == 'published' and self.published_date is None or '':
      self.published_date = timezone.now()
    elif self.status == 'published' and self.published_date is not None or '':
      self.updated_date = timezone.now()
    super(Post, self).save()


  def get_author(self):
    """
    get user's full name or username
    """
    if self.author.first_name and self.author.last_name:
      return "%s %s" % (self.author.first_name, self.author.last_name)
    else: 
      return self.author.username


  class Meta:
    """ define metadata options for the Post model """
    ordering = ('-published_date',) # set default ordering of the objects

  def __str__(self):
    """ identify blog entries by their title for admin page """
    return self.title


  @permalink
  def get_post_detail_url(self):
    return ('post_detail', [self.published_date.year,
                            self.published_date.month,
                            self.slug])