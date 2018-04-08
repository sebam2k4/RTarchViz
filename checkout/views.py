# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import MakePaymentForm, OrderForm

# Create your views here.

@login_required
def checkout(request):
  payment_form = MakePaymentForm()
  order_form = OrderForm()
  context = {'payment_form': payment_form, 'order_form': order_form}

  return render(request, "checkout.html", context)