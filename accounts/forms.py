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
  A form to handle editing of user details.

  Usename is case sensitive, but unique in a way that no two users
  can have same letters usernames no matter what letter case. If a
  user has a username 'JoHn' then another user cannot register or
  change their username to 'john'.

  email is always saved in db in lowercase no matter how it was entered
  and all validation checks are case insensitive.
  """
  def clean_username(self):
    """
    Allow user to change letter case on their username or change 
    username to a different one provided it isn't registered by another
    user.
    Checks if username already registered by case insensitive check
    """
    current_user = self.instance
    new_username = self.cleaned_data.get('username')
    if current_user.username.lower() != new_username.lower():
      if User.objects.filter(username__iexact=new_username):
        message = "Username already registered!"
        raise ValidationError(message)
    else:
      return new_username

  class Meta:
    model = User
    fields = ['email', 'username', 'first_name', 'last_name', 'bio', 'birth_date', 'address1',
              'address2', 'city_town', 'county_state', 'post_code', 'country']

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
    fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'bio',
              'birth_date', 'address1', 'address2', 'city_town', 'county_state', 'post_code',
              'country']

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
