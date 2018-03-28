# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from .models import Product


def products_list(request):
  products = Product.objects.all()
  return render(request, "products_list.html", {"products": products})

# def product_detail(request):
#   products = Product.objects.all()
#   return render(request, "products_list.html", {"products": products})