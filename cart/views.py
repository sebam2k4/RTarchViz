# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from checkout.models import Order
from django.contrib import messages

# Create your views here.
@login_required
def view_cart(request):
  """ A view that renders the cart contents page """

  return render(request, 'cart.html')

@login_required
def add_to_cart(request, product_id):
  """ Add product to cart """
  previous_page = request.META.get('HTTP_REFERER')
  
  # get list of already purchased assets
  orders = Order.objects.filter(buyer_id=request.user.id)
  owned_assets = []
  for order in orders:
    for item in order.products.all():
      owned_assets.append(item)

  product = get_object_or_404(Product, pk=product_id)
  # retrieve session key for cart and its contents in a dictionary
  cart = request.session.get('cart', {})

  if product_id in cart:
    messages.error(request, 'Item already in cart')
    #return redirect(reverse('products_list'))
    return redirect(previous_page)

  elif product.seller == request.user:
    messages.error(request, 'Nice try! You can\'t buy your own product...')
    #return redirect(reverse('products_list'))
    return redirect(previous_page)

  # check if you already own this product
  elif product in owned_assets:
    messages.error(request, 'You already own this product!')
    #return redirect(reverse('products_list'))
    return redirect(previous_page)

  else:
    # add product to cart session
    cart[product_id] = cart.get(product_id, product.slug)
    messages.success(request, 'Added \'{0}\' to your cart'.format(product.name))
    # save session with new cart contents
    request.session['cart'] = cart
    #return redirect(reverse('view_cart'))
    return redirect(previous_page)

@login_required
def clear_cart(request):
  """ Remove all product items from cart """
  request.session['cart'] = {}
  messages.success(request, 'Removed all items from cart')
  return redirect(reverse('view_cart'))

@login_required
def remove_cart_item(request, product_id):
  """ Remove single product item """
  cart = request.session.get('cart', {})

  if product_id in cart:
    cart.pop(product_id)
    messages.success(request, 'Successfully removed item')

  request.session['cart'] = cart
  return redirect(reverse('view_cart'))
