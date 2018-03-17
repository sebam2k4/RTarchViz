# -*- coding: utf-8 -*-

from models import User

# Created EmailAuth class that will replace the standard 'auth' object that Django uses
# to check logins, and override two of its default methods. Authenticate by email, not username

class EmailAuth(object):
  '''Authenticate a user by an exact match on the email and password'''
  def authenticate(self, email=None, password=None):
    '''
    Get an instance of User based off the supplied email and verify password
    (finding the user by email and not the default's username)
    '''
    try:
      user = User.objects.get(email=email)
      if user.check_password(password):
        return user
    except User.DoesNotExist:
      return None
  
  def get_user(self, user_id):
    '''
    Used by the django authentication system to retrieve an instance of User
    and make sure user is active and whether they can log in.
    * Can apply extra conditions to the login process, ex: user ban,
    disabling accounts after non-login time, etc.
    '''
    try:
      user = User.objects.get(pk=user_id)
      if user.is_active:
        return user
      return None
    except User.DoesNotExist:
      return None
