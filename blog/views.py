# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone
from .models import Post

def filter_posts(request):
  published_posts = Post.objects.published()
  if request.GET['filter-select'] == 'oldest':
    published_posts = published_posts.order_by('published_date')
  if request.GET['filter-select'] == 'most popular':
    published_posts = published_posts.order_by('view_count')
  if request.GET['filter-select'] == 'tutorials':
    published_posts = published_posts.filter(category='tutorial')
  if request.GET['filter-select'] == 'news':
    published_posts = published_posts.filter(category='news')

  return render(request, 'posts_list.html', {"posts": published_posts})



def posts_list(request):
  print request
  '''
  Create a view that will return a list of all published posts
  and render them to the 'blogposts.html' template.

  '''
  # Get all published posts
  published_posts = Post.objects.published()

  # set up pagination (4 posts per page)
  paginator = Paginator(published_posts, 4)
  blog_page= request.GET.get('page')
  try:
    posts = paginator.page(blog_page)
  except PageNotAnInteger:
    # if page is not an integer, deliver first page
    posts = paginator.page(1)
  except EmptyPage:
    # deliver last page of results if page is out of range
    posts = paginator.page(paginator.num_pages)
  return render(request, 'posts_list.html', {'posts': posts, 'paginator': paginator})

def post_detail(request, year, month, slug):
  '''
  Create a view that returns a single Post object based
  on the post published year, month, and slug and render
  it to the 'postdetail.html' template.
  Or return a 404 error if the post is not found.
  '''
  post = get_object_or_404(Post, published_date__year=year, published_date__month=month, slug=slug)
  
  next_post = Post.objects.get_next_post(post.published_date)   
  prev_post = Post.objects.get_prev_post(post.published_date)   

  # remove the page view counter to prevent other logic from running on post.save
  # need to implement the counter in a different way - session based?
  #post.view_count += 1 # clock up the number of post views
  #post.save()
  return render(request, "post_detail.html", {'post': post, 'next_post': next_post, 'prev_post': prev_post})