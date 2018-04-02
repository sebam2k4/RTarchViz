from django.conf.urls import url
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.views import password_reset, password_reset_done, password_reset_confirm, password_reset_complete

urlpatterns = [
  url(r'^password_reset/$', password_reset,
         {'post_reset_redirect': reverse_lazy('password_reset_done')}, name='password_reset'),
  url(r'^password_reset/done/$', password_reset_done, name='password_reset_done'),
  url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         password_reset_confirm, {'post_reset_redirect': reverse_lazy('password_reset_complete')},
         name='password_reset_confirm'),
  url(r'^reset/done/$', password_reset_complete, name='password_reset_complete'),
]
