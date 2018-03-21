# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post

def posts_list(request):
  print request
  '''
  Create a view that will return a list of Posts
  that were published prior to 'now'
  and render them to the 'blogposts.html' template
  '''
  # Get all published posts
  published_posts = Post.objects.published().all()
    
  return render(request, 'posts_list.html', {'posts': published_posts})