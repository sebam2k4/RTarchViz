# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone
from django.utils.html import strip_tags
from django.db.models import permalink
from django.db.models.signals import post_save
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from django.dispatch import receiver


class PostManager(models.Manager):
    """Defining custom Manager methods"""

    def published(self):
        """ elect only published posts"""
        return self.get_queryset().filter(status="published")


class Post(models.Model):
    """Defining Blog's Post models"""

    # CHOICES:
    CATEGORY_CHOICES = (
        ('news', 'News'),
        ('tutorial', 'Tutorial')
    )
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published')
    )

    # DATABASE FIELDS:
    # author is linked to a registered staff user, via the User model in
    # the accounts app.
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    title = models.CharField(max_length=200, unique=True)
    # slug is generated from the title
    slug = models.SlugField(editable=False, max_length=200, unique=True)
    content = models.TextField(max_length=10000)
    # identify when post was created
    created_date = models.DateTimeField(editable=False, default=timezone.now)
    # set publish date initially to blank and null as drafts are allowed
    # published date will be set once post is published
    published_date = models.DateTimeField(
        editable=False, blank=True, null=True)
    # record when a published post is last edited
    updated_date = models.DateTimeField(editable=False, blank=True, null=True)
    # set post's category
    category = models.CharField(
        max_length=10, choices=CATEGORY_CHOICES, default='news')
    # set post's status (draft or published)
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default='draft')
    # add images to a post (stores relative path to image)
    image = models.ImageField(upload_to="images", blank=True, null=True)

    # MANAGERS:
    objects = PostManager()

    # META CLASS:
    class Meta:
        """ specify global meta options for model """
        # order by descending date (most recent posts first)
        ordering = ('-published_date',)

    # TO STRING METHOD:
    def __unicode__(self):
        """ specify string representation for a post in admin pages """
        return self.title

    def clean(self):
        """ clean data before saving in db """
        self.title = self.title.capitalize()

    # SAVE METHOD:
    def save(self, *args, **kwargs):
        """
        overwrite Model save method to 
        1. automatically generate a slug from post's title
        2. set published_date with current date & time when post's
           status is initially changed from 'draft' to 'published'
        3. set updated_date with current date & time if published_date
           already set
        """
        self.slug = slugify(self.title)
        if self.status == 'published' and self.published_date is None:
            self.published_date = timezone.now()
        elif self.status == 'published' and self.published_date is not None:
            self.updated_date = timezone.now()
        super(Post, self).save()

    # ABSOLUTE URL METHODS:
    def get_absolute_url(self):
        return reverse('post_detail', args=[self.published_date.year,
                                            self.published_date.month,
                                            self.slug])

    # CUSTOM MODEL METHODS:
    def get_author(self):
        """get user's full name or username"""
        if self.author.first_name and self.author.last_name:
            return "{0} {1}".format(self.author.first_name,
                                    self.author.last_name)
        return self.author.username

    def get_short_content(self):
        """get truncated & html tags stripped post's content for admin """
        return truncatechars(strip_tags(self.content), 124)


class PostViewCount(models.Model):
    """Defining PostViewCount model - keeps count of post views"""

    # use one-to-one field to link it to specific blog post
    post = models.OneToOneField(Post)
    # record how often a post is seen
    view_count = models.IntegerField('views', editable=False, default=0)

    # TO STRING METHOD:
    def __unicode__(self):
        """ specify string representation for a post in admin pages """
        return 'Views: {0}'.format(str(self.view_count))


# SIGNALS
@receiver(post_save, sender=Post)
def create_post_view_count(sender, instance, created, **kwargs):
    """ 
    When creating Post model instance also create PostViewCount
    model instance for keeping post view counts
    """
    if created:
        PostViewCount.objects.create(post=instance)
