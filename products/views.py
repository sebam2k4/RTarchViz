# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


def products_list(request):
  """
  This view does two tings:

  1. returns a list of all products and render them
  to the 'products_list.html' template.

  2. Provides filtering by category and various ordering choices
  to user through 2 select fields in the template: When user
  applies a filer, a get request is made with the user's choices as a query string and is matched with one of the predefined category or ordering
  options defined below.
  """
  products = Product.objects.all()

  # define filter choices and get filtered objects based on user select
  # note: refactor this code as it pretty much uses all hard coded values. See
  #       if can fill a tuple from a list of available product categories?
  #       This would be useful for when categories are added or modified.
  category_choices = ('all products', 'assets', 'environment', 'blueprint', 'materials')
  order_choices = ('newest', 'oldest', 'most popular', 'a-z', 'z-a')

  
  if request.method == 'GET':
    chosen_category = request.GET.get('product-category-select')
    chosen_order = request.GET.get('product-order-select')
    
    if chosen_category:
      if chosen_category == 'all products':
        products_by_category = products
      else:
        products_by_category = products.filter(category=chosen_category)
      #products = products_by_category

    if chosen_order:
      if chosen_order == 'newest':
        products_by_ordering = products_by_category.order_by('-added_date')
      elif chosen_order == 'oldest':
        products_by_ordering  = products_by_category.order_by('added_date')
      elif chosen_order == 'most popular':
        products_by_ordering = products_by_category.order_by('-sold_count')
      elif chosen_order == 'a-z':
        products_by_ordering = products_by_category.order_by('name')
      elif chosen_order == 'z-a':
        products_by_ordering = products_by_category.order_by('-name')
      products = products_by_ordering

  return render(request, 'products_list.html', {'products': products, 'category_choices': category_choices, 'order_choices': order_choices, 'chosen_order': chosen_order, 'chosen_category': chosen_category})

def product_detail(request, slug, id):
  """
  A view that returns a single product object based on product's
  slug and id and renders it to the 'product_detail.html' template.
  Or return a 404 error if the product is not found.
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  # clock up the number of product views
  product.view_count += 1
  product.save()
  return render(request, "product_detail.html", {"product": product})

def new_product(request):
  """
  A view that allows to create a new product
  """
  if request.method == "POST":
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      product = form.save(commit=False)
      product.seller = request.user
      product.save()
      return redirect(Product.get_product_detail_url(product))
  else:
    form = ProductForm()
  # Render the new product
  return render(request, 'product_form_new.html', {'form': form})

def edit_product(request, slug, id):
  """
  A view that allows to edit an existing product
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  if request.method == "POST":
    # Create instance of ProductForm & bind file data and form data
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
      product = form.save(commit=False)
      product.seller = request.user
      product.save()
      return redirect(Product.get_product_detail_url(product))
  else:
    # Render the edited product
    form = ProductForm(instance=product)
  return render(request, 'product_form_edit.html', {'form': form})
  