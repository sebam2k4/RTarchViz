# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from .forms import ProductForm


def products_list(request):
  """
  A view that returns a list of all products and render them
  to the 'products_list.html' template.
  """
  products = Product.objects.all()
  return render(request, "products_list.html", {"products": products})

def product_detail(request, slug, id):
  """
  A view that returns a single product object based on product's
  slug and id and renders it to the 'product_detail.html' template.
  Or return a 404 error if the product is not found.
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
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
  return render(request, 'product_form_new.html', {'form': form})

def edit_product(request, slug, id):
  """
  A view that allows to edit an existing product
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  if request.method == "POST":
    # Create instance of ProductForm & bind file data and form data
    # https://docs.djangoproject.com/en/1.11/ref/forms/api/#binding-uploaded-files
    form = ProductForm(request.POST, request.FILES, instance=product)
    if form.is_valid():
      product = form.save(commit=False)
      product.seller = request.user
      product.save()
      return redirect(Product.get_product_detail_url(product))
  else:
    form = ProductForm(instance=product)
  return render(request, 'product_form_edit.html', {'form': form})