# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import csrf
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import User
from products.models import Product
from checkout.models import Order


# Create your views here.
def register(request):
  """
  View to take the new user's email and password. When validated,
  create the account.
  """
  # redirect to user's profile page is user already authenticated
  if request.user.is_authenticated:
    return redirect(User.get_absolute_url(request.user))

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
        return redirect(User.get_absolute_url(request.user))
      else:
        messages.error(request, "unable to log you in at this time!")

  else:
    form = UserRegistrationForm()

  context = {'form': form}
  context.update(csrf(request))
  return render(request, 'register.html', context)


def login(request):
  """
  View to show default email/password login form and validate the input
  """
  # redirect to profile page is user already authenticated
  if request.user.is_authenticated:
    return redirect(User.get_absolute_url(request.user))

  if request.method == 'POST':
    # use Django's built in auth.login method for user login
    form = UserLoginForm(request.POST)
    if form.is_valid():
      # validate the input before using the auth object
      user = auth.authenticate(email=request.POST.get('email').lower(),
                               password=request.POST.get('password'))
      if user is not None:
        auth.login(request,user)
        messages.success(request, "You have successfully logged in")
        return redirect(User.get_absolute_url(request.user))
      else:
        form.add_error(None, "Your email or password was not recognised")
  else:
    form = UserLoginForm()

  context = {'form': form}
  context.update(csrf(request))
  return render(request, 'login.html', context)

def profile(request, username):
  """
  A view that gets the specified user object based on username
  and renders it to the 'profile.html' template. Also, gets the
  user's products.
  """
  user = get_object_or_404(User, username=username)
  
  context = {'user': user}
  return render(request, 'profile.html', context)

def user_list(request):
  """
  A view for listing all registered users (for testing)
  """
  users = User.objects.all()

  context = {'users': users}
  return render(request, 'users_list.html', context)

@login_required
def dashboard(request):
  """
  A view that gets the authenticated user's dashboard and provides stats
  on product sales and purchases as well as interface for adding
  products, editing user personal details, and changing user password.
  """
  user = User.objects.get(email=request.user.email)

  # get products user has listed for sale
  products = Product.objects.filter(seller_id = user.id).order_by('-added_date')

  context = {'user': user, 'products': products}
  return render(request, 'dashboard.html', context)

@login_required
def logout(request):
  # destroy user session with .logout method
  auth.logout(request)
  messages.success(request, 'You have successfully logged out')
  return redirect(reverse('homepage'))

@login_required
def update(request):
  """
  Update User profile details. Uses an instance of user data to fill in
  the form fields with current data.
  """
  if request.method == 'POST':
    form = UserEditForm(data=request.POST, instance=request.user)
    if form.is_valid():
      form.save()
      messages.success(request, 'You have successfully Updated your details')
      return redirect(reverse('dashboard'))
    else:
      messages.error(request, 'Please correct the error!')
  else:
    form = UserEditForm(instance=request.user)

  context = {'form': form}
  return render(request, 'update.html', context)

@login_required
def change_password(request):
  """
  change password for authenticated user using Django's built in
  PasswordChangeForm.
  """
  if request.method == 'POST':
    form = PasswordChangeForm(user=request.user, data=request.POST)
    if form.is_valid():
      user = form.save()
      # update session auth hash otherwise user will be logged out after
      # password change
      update_session_auth_hash(request, user=request.user)
      messages.success(request, 'Your password was successfully updated!')
      return redirect(User.get_absolute_url(request.user))
    else:
      messages.error(request, 'Please correct the errors!')
  else:
    form = PasswordChangeForm(user=request.user)

  context = {'form': form}
  return render(request, 'change_password.html', context)
