# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
  email = forms.EmailField(widget=forms.EmailInput(attrs={'autofocus': True}),)
  password = forms.CharField(widget=forms.PasswordInput)

class UserEditForm(forms.ModelForm):
  """
  A form to handle editing of user details. Performs case insensitive check
  for email and username to make sure they're not already registered.
  """

  # Note: validation error when form saved without changing the email & username fields
  #       need some sort of check if these fields changed or not.
  def clean_email(self):
    """
    Check if email already registered (case insensitive check)
    """
    email = self.cleaned_data.get('email')
    if User.objects.filter(email__iexact=email):
      message = "Email already registered!"
      raise ValidationError(message)
    return email

  def clean_username(self):
    """
    Check if username already registered (case insensitive check)
    """
    username = self.cleaned_data.get('username')
    if User.objects.filter(username__iexact=username):
      message = "Username already registered!"
      raise ValidationError(message)
    return username

  class Meta:
    model = User
    fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'birth_date', 'address1', 'address2', 'city_town', 'county_state', 'post_code', 'country']

class UserRegistrationForm(UserCreationForm):
  """
  Extending UserCreationForm
  Performs case insensitive check for email and username to make sure
  they're not already registered.
  """
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

  password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

  class Meta:
    model = User
    fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'address1', 'address2', 'city_town', 'county_state', 'post_code', 'country'] #only display these input fields

  def clean_email(self):
    """
    Check if email already registered (case insensitive check)
    """
    email = self.cleaned_data.get('email')
    if User.objects.filter(email__iexact=email):
      message = "Email already registered!"
      raise ValidationError(message)
    return email

  def clean_username(self):
    """
    Check if username already registered (case insensitive check)
    """
    username = self.cleaned_data.get('username')
    if User.objects.filter(username__iexact=username):
      message = "Username already registered!"
      raise ValidationError(message)
    return username




