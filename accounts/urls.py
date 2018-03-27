"""auth_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
import views
from . import url_reset


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/update/$', views.update, name='update'),
    url(r'^profile/password_change/$', views.change_password, name='change_password'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'password/', include(url_reset)),
    url(r'^profile/user/(?P<username>[\w.@+-]+)/?$', views.profile, name='profile'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/user/$', views.user_list, name='user_list'),
]
