# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.decorators import login_required
from .models import User

# Create your views here.
def register(request):
  '''
  View to take the new user's email and password. When validated,
  create the account.
  '''
  # redirect to profile page is user already authenticated
  if request.user.is_authenticated:
    return redirect(reverse('profile'))

  if request.method == 'POST':
    form = UserRegistrationForm(request.POST)
    if form.is_valid():
      form.save()

      # *using the replaced auth object from backends.py
      user = auth.authenticate(email=request.POST.get('email').lower(),
                                password=request.POST.get('password1'))

      if user:
        messages.success(request, "You have successfully registered")
        auth.login(request,user) # login automatically after registering
        return redirect(reverse('profile'))
      else:
        messages.error(request, "unable to log you in at this time!")

  else:
    form = UserRegistrationForm()

  args = {'form': form}
  args.update(csrf(request))

  return render(request, 'register.html', args)


def login(request):
  '''
  View to show default email/password login form and validate the input
  '''
  # redirect to profile page is user already authenticated
  if request.user.is_authenticated:
    return redirect(reverse('profile'))

  if request.method == 'POST':
    # use Django's built in auth.login method for user login
    form = UserLoginForm(request.POST)
    if form.is_valid():
      # validate the input before using the auth object
      user = auth.authenticate(email=request.POST.get('email').lower(), # lowercase user input
                                password=request.POST.get('password'))

      if user is not None:
        auth.login(request,user)
        messages.success(request, "You have successfully logged in")
        return redirect(reverse('profile'))
      else:
        form.add_error(None, "Your email or password was not recognised")

  else:
    form = UserLoginForm()

  args = {'form': form}
  args.update(csrf(request))
  return render(request, 'login.html', args)


# restrict access to logged in users
@login_required
def profile(request):
  '''
  User profile page view
  '''
  user = User.objects.get(email=request.user.email)
  
  return render(request, 'profile.html', {"profile": user})

@login_required
def logout(request):
  auth.logout(request) # destroy user session with .logout method
  messages.success(request, 'You have successfully logged out')
  return redirect(reverse('index'))