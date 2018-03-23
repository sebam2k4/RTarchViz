# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post

def posts_list(request):
  '''
  A view that returns a paginated list of all published posts and
  renders them to the 'posts_list.html' template. 
  
  Also, provides filtering and ordering choices to user through a
  select field in the template: When user applies a filer, a get
  request is made with the user's choice as a query string and is
  matched with one of the predefined options below (oldest,
  turtorials, news, or most popular).
  
  This view is dealing with up to two query strings at the same
  time, one for pagination '?page=' and another for filter
  '?post-filter-select=' To avoid the filter query string from
  being cleared by requesting next page of results with paginator,
  the form's select option in the template has to be matched with
  user selected filter and set 'selected' attribute on the specified
  option tag.
  '''
  # Get all published posts
  published_posts = Post.objects.published()

  # define filter choices and get filtered objects based on user select
  filter_choices = ('newest', 'oldest', 'tutorials', 'news', 'most popular')
  chosen_filter = request.GET.get('post-filter-select')
  if chosen_filter == 'oldest':
    published_posts = published_posts.order_by('published_date')
  if chosen_filter == 'tutorials':
    published_posts = published_posts.filter(category='tutorial')
  if chosen_filter == 'news':
    published_posts = published_posts.filter(category='news')
  if chosen_filter == 'most popular':
    published_posts = published_posts.order_by('view_count')
  
  # set up pagination (4 posts per page)
  paginator = Paginator(published_posts, 4)
  blog_page = request.GET.get('page')
  try:
    posts = paginator.page(blog_page)
  except PageNotAnInteger:
    # if page is not an integer, deliver first page
    posts = paginator.page(1)
  except EmptyPage:
    # deliver last page of results when page is out of range
    posts = paginator.page(paginator.num_pages)
  return render(request, 'posts_list.html', {'posts': posts, 'paginator': paginator, 'filter_choices': filter_choices, 'chosen_filter': chosen_filter})

def post_detail(request, year, month, slug):
  '''
  A view that returns a single Post object based
  on the post's published year, month, and slug and renders
  it to the 'postdetail.html' template. Or return a 404
  error if the post is not found.

  The view also gets the next and previous post through a
  query set defined in the custom PostManager
  '''
  post = get_object_or_404(Post, published_date__year=year, published_date__month=month, slug=slug)
  
  # get the next post and get the previous post
  next_post = Post.objects.get_next_post(post.published_date)   
  prev_post = Post.objects.get_prev_post(post.published_date)   

  # remove the page view counter to prevent other logic from running on post.save (I've overriden object's save method to do timestamps)
  # need to implement the counter in a different way - session based?
  #post.view_count += 1 # clock up the number of post views
  #post.save()

  return render(request, "post_detail.html", {'post': post, 'next_post': next_post, 'prev_post': prev_post})