# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
  email = forms.EmailField()
  password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
  """
  Extending UserCreationForm
  Unique Fields: Email, Username
  """
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

  password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

  # require email field
  # def __init__(self, *args, **kwargs):
  #   super(UserRegistrationForm, self).__init__(*args, **kwargs)
  #   self.fields['email'].required = True

  class Meta:
    model = User
    fields = ['email', 'username', 'password1', 'password2', 'first_name', 'last_name', 'birth_date', 'address1', 'address2', 'city_town', 'post_code', 'country'] #only display these input fields

  def clean_password2(self):
    """
    Custom method to do data cleaning on passwords and
    basic validation to check if passwords match -
    May add min length, special chars, etc.
    """
    password1 = self.cleaned_data.get('password1')
    password2 = self.cleaned_data.get('password2')
    
    if not password1 or not password2:
      message = "Please confirm your password"
      raise ValidationError(message)

    if password1 != password2:
      message = "Passwords do not match"
      raise ValidationError(message)

    return password2

  def clean_email(self):
    """
    Check if email already registered (case insensitive check)
    """
    # get the email
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




