# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.core.exceptions import ValidationError

class UserLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(UserCreationForm):
  password1 = forms.CharField(label='Password', widget=forms.PasswordInput)

  password2 = forms.CharField(label='Password Confirmation', widget=forms.PasswordInput)

  # require email field
  # def __init__(self, *args, **kwargs):
  #   super(UserRegistrationForm, self).__init__(*args, **kwargs)
  #   self.fields['email'].required = True

  class Meta:
    model = User
    fields = ['email', 'username', 'password1', 'password2', 'first_name'] #only display these input fields

  def clean_password2(self):
    '''
    Custom method to do data cleaning on passwords and
    basic validation to check if passwords match -
    May add min length, special chars, etc.
    '''
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
    '''
    Check if email already registered
    '''
    # get the email
    email = self.cleaned_data.get('email')
    # username = self.cleaned_data.get('username') # no need to clean as assigned email when form submit
    # check to see if any users already exist with this email
    if User.objects.filter(email=email):
      message = "Email already registered!"
      raise ValidationError(message)

    return email
    # try:
    #   email = User.objects.get(email=email)
    #   message = "Email already registered!"
    # except User.DoesNotExist:
    #   # Unable to find a user, register the new user
    #   return email

    # found registered email so raise an error
    # print "hello"
    # raise ValidationError(message)



