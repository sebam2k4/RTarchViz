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
  published_posts = Post.objects.published()
  print published_posts[0].id
  return render(request, 'posts_list.html', {'posts': published_posts})

def post_detail(request, year, month, slug):
  '''
  Create a view that returns a single Post object based
  on the post published year, month, and slug and render
  it to the 'postdetail.html' template.
  Or return a 404 error if the post is not found.
  '''
  post = get_object_or_404(Post, published_date__year=year, published_date__month=month, slug=slug)
  post.views_count += 1 # clock up the number of post views
  post.save()
  return render(request, "post_detail.html", {'post': post})