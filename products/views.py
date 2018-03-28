# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from .models import Product


def products_list(request):
  products = Product.objects.all()
  return render(request, "products_list.html", {"products": products})

def product_detail(request, id):
  product = get_object_or_404(Product, pk=id)
  return render(request, "product_detail.html", {"product": product})