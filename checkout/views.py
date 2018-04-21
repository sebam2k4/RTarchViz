# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm
from django.conf import settings
from django.utils import timezone
from products.models import Product
from .models import OrderProduct, Order, PurchaseHistory
import stripe


stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
  if request.method=="POST":
    payment_form = MakePaymentForm(request.POST)

    if payment_form.is_valid():
      cart = request.session.get('cart', {})
      total = 0
      product_count = 0
      for id in cart:
        product = get_object_or_404(Product, pk=id)
        total += product.price
        product_count += 1

      try:
        # capture one time payment
        customer = stripe.Charge.create(
                    amount=int(total * 100),
                    currency="EUR",
                    description=request.user.email,
                    card=payment_form.cleaned_data['stripe_id']
        )
      # STRIPE exception
      except stripe.error.CardError, e:
        messages.error(request, "Your card was declined")

      if customer.paid:
        timestamp = timezone.now()

        order = Order()
        # add data to Order instance
        order.ordered_date = timestamp
        order.buyer = request.user
        order.total_amount = total
        order.product_count = product_count
        order.save()
   
        for id in cart:
          product = get_object_or_404(Product, pk=id)
          # count up sold_count for each product
          product.sold_count += 1
          product.save()
          order_product_item = OrderProduct(order=order, product=product,)
          order_product_item.save()
          # record purchase transactio history for each product
          purchase = PurchaseHistory()
          purchase.product_price = product.price
          purchase.product_name = product.name
          purchase.date = timestamp
          purchase.seller_id = product.seller_id
          purchase.buyer_id = request.user.id
          purchase.product_file = product.product_file
          purchase.product_id = product.id
          purchase.order_id = order.id
          purchase.save()

        # copy cart session into purchase session storage
        request.session['purchase'] = request.session['cart']
        # clear cart session
        request.session['cart'] = {}
        messages.success(request, "Your purchase was successful!")
        return redirect('thank_you')
      else:
        messages.error(request, "Unable to take payment")
    
    else:
      print(payment_form.errors)
      messages.error(request, "We were unable to take a payment with that card!")
  else:
    payment_form = MakePaymentForm()
      
  context = {'payment_form': payment_form, 'publishable': settings.STRIPE_PUBLISHABLE}

  return render(request, "checkout.html", context)

@login_required
def thank_you(request):
  """
  Displays thank you page. Uses purchase session to list purchased
  products.
  """
  purchase = request.session.get('purchase')
  purchase_items = []
  for id in purchase:
    product = get_object_or_404(Product, pk=id)
    purchase_items.append(product)

  request.session['purchase'] = {}

  context = {'purchase_items': purchase_items}
  return render(request, "thank_you.html", context)