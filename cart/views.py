# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from checkout.models import Order
from django.contrib import messages
from django.template import RequestContext
from django.http import JsonResponse


def view_cart(request):
    """ A view that renders the cart contents page """

    return render(request, 'cart.html')


def add_to_cart(request, product_id):
    """ Add product to cart """
    
    product = get_object_or_404(Product, pk=product_id)
    # retrieve session key for cart and its contents in a dictionary
    cart = request.session.get('cart', {})

    # get previous page
    if request.META.get('HTTP_REFERER') is not None:
        previous_page = request.META.get('HTTP_REFERER')
    else:
        previous_page = 'products_list'

    # get a list of user's purchased products
    user_owned_products = Order.objects.purchased_products(request.user)

    if product_id in cart:
        message = 'Item already in cart'
        if not request.is_ajax():
            messages.error(request, message)
        product_added = False

    elif product.seller == request.user:
        message = 'Nice try! You can\'t buy your own product...'
        if not request.is_ajax():
            messages.error(request, message)
        product_added = False

    # check if you already own this product
    elif product in user_owned_products:
        message = 'You already own this product!'
        if not request.is_ajax():
            messages.error(request, message)
        product_added = False
    else:
        # add product to cart session
        cart[product_id] = cart.get(product_id, product.slug)
        product_added = True
        message = 'Added \'{0}\' to your cart'.format(product.name)
        if not request.is_ajax():
            messages.success(request, message)
        # save session with new cart contents
        request.session['cart'] = cart
    
    if request.is_ajax():
        json_data = {
            "added": product_added,
            "cartItemsCount": len(cart),
            "message": message

        }
        return JsonResponse(json_data)

    # return previous page when js disabled
    return redirect(previous_page)


def clear_cart(request):
    """ Remove all product items from cart """
    request.session['cart'] = {}
    messages.success(request, 'Removed all items from cart')
    return redirect(reverse('view_cart'))


def remove_cart_item(request, product_id):
    """ Remove single product item """
    cart = request.session.get('cart', {})

    if product_id in cart:
        cart.pop(product_id)
        messages.success(request, 'Successfully removed item')

    request.session['cart'] = cart
    return redirect(reverse('view_cart'))
