# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.utils import timezone
from django.urls import reverse


class AccountUserManager(UserManager):
    """ Custom User Manager """
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email, and
        password
        """
        if not email:
            raise ValueError('The given email address must be set')
        if not username:
            raise ValueError('The given username must be set')

        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,
                          is_staff=is_staff,
                          is_active=True,
                          is_superuser=is_superuser,
                          date_joined=timezone.now(),
                          **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def normalize_email(cls, email):
        """
        Normalize the address by lowercasing both the name and domain
        parts of the email address before saving it to the db.
        """
        email = email or ''
        try:
            email_name, domain_part = email.strip().rsplit('@', 1)
        except ValueError:
            pass
        else:
            email = '@'.join([email_name.lower(), domain_part.lower()])
        return email


class User(AbstractUser):
    """
    User inherits from Django's AbstractUser class.
    Adding custom attributes for billing address and stripe payments
    """

    # DATABASE FIELDS:
    email = models.EmailField(max_length=150, unique=True, blank=False)
    bio = models.TextField('Bio', max_length=750, blank=True)
    birth_date = models.DateField('Date of Birth', null=True, blank=True,
                                  help_text='YYYY-MM-DD format')
    address1 = models.CharField('Address Line 1', max_length=100, blank=True)
    address2 = models.CharField('Address Line 2', max_length=100, blank=True)
    city_town = models.CharField('City or Town', max_length=100, blank=True)
    county_state = models.CharField('County or State', max_length=100,
                                    blank=True)
    post_code = models.CharField('Post Code', max_length=20, blank=True)
    country = models.CharField('Country', max_length=100, blank=True)
    # Stripe id for processing payments
    stripe_id = models.CharField(max_length=40, default='', blank=True)

    # MANAGERS:
    objects = AccountUserManager()

    # TO STRING METHOD:
    def __unicode__(self):
        """ specify string representation for a user in admin pages """
        return self.username

    def get_absolute_url(self):
        return reverse('profile', args=[self.username])
