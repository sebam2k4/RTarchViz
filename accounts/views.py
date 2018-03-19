# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages, auth
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf
from .forms import UserRegistrationForm, UserLoginForm, UserEditForm
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required
from .models import User
# from django.http import HttpResponseRedirect

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
      return redirect('update')
  else:
    form = UserEditForm(instance=request.user)
  args = {'form': form}
  return render(request, 'update.html', args)

@login_required
def change_password(request):
  """
  Change password for the authenticated user
  """
  if request.method == 'POST':
    form = PasswordChangeForm(request.user, request.POST)
    if form.is_valid():
      user = form.save()
      # update session auth hash otherwise user will be logged out after password change
      update_session_auth_hash(request, user)
      messages.success(request, 'Your password was successfully updated!')
      return redirect('change_password')
    else:
      messages.error(request, 'Please correct the error below.')
  else:
    form = PasswordChangeForm(request.user)
  return render(request, 'change_password.html', {'form': form})



# Could use something like this for extra security for profile edit and password change views?:
# from django.core.exceptions import PermissionDenied
#   # querying the User object with pk from url
#   user = User.objects.get(pk=pk)
#   if request.user.is_authenticated() and request.user.id == user.id:
#     ...
#   else:
#     raise PermissionDenied