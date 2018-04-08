# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import MakePaymentForm, OrderForm
from django.conf import settings
from django.utils import timezone
from products.models import Product
from .models import OrderProduct
import stripe


stripe.api_key = settings.STRIPE_SECRET

@login_required
def checkout(request):
  if request.method=="POST":
    payment_form = MakePaymentForm(request.POST)
    order_form = OrderForm(request.POST)

    if payment_form.is_valid() and order_form.is_valid():
      cart = request.session.get('cart', {})

      order = order_form.save(commit=False)
      order.ordered_date = timezone.now()
      order.buyer = request.user
      
      total = 0
      product_count = 0
      for id in cart:
        product = get_object_or_404(Product, pk=id)
        total += product.price
        product_count += 1

      order.total_amount = total
      order.product_count = product_count
      order.save()

      for id in cart:
        product = get_object_or_404(Product, pk=id)
        order_product_item = OrderProduct(order = order, product = product,)
        order_product_item.save()

      

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

      # Register user when payment successful:
      if customer.paid:
        request.session['cart'] = {}
        messages.success(request, "Your purchase was successful! You'll get your product link soon.")
        return redirect(reverse('profile', args=[request.user.username]))
      else:
        messages.error(request, "Unable to take payment")
    
    else:
      print(payment_form.errors)
      print(order_form.errors)
      messages.error(request, "We were unable to take a payment with that card!")
  else:
    payment_form = MakePaymentForm()
    order_form = OrderForm()
      
  context = {'payment_form': payment_form, 'order_form': order_form, 'publishable': settings.STRIPE_PUBLISHABLE}

  return render(request, "checkout.html", context)