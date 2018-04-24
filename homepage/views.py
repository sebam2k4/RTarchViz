# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.mail import send_mail
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages

# Create your views here.

def homepage(request):
  return render(request, 'index.html')
  
def newsletter_signup(request):
  """
  Send confirmation email for signing up to newsletter
  """
  # get previous page or index
  if request.META.get('HTTP_REFERER') is not None:
    previous_page = request.META.get('HTTP_REFERER')
  else:
    previous_page = 'index.html'
  email = request.POST.get('newsletter_signup_email')
  if request.method == 'POST':
    email = request.POST.get('newsletter_signup_email')
    recipient_list = [email]
    print recipient_list
    subject = "Thank you for signing up to RTarchViz's Newsletter!"
    message = "Get ready for the latest and greatest news about Unreal Engine 4 assets, techniques, and news! archviz.herokuapp.com"
    from_email = settings.EMAIL_HOST_USER
    print from_email
    send_mail(subject, message, from_email, recipient_list,)
    messages.success(request, 'Thank You! You\'ve signed up to our Newsletter. Check Your Email')
  return redirect(previous_page)