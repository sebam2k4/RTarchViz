from django.conf.urls import url, include
import views
from . import url_reset


urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^profile/update/$', views.update_profile, name='update'),
    url(r'^profile/password_change/$', views.change_password, name='change_password'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'password/', include(url_reset)),
    url(r'^profile/user/(?P<username>[\w.@+-]+)/?$', views.profile, name='profile'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^dashboard/purchases_history/$', views.purchases_history, name='purchases_history'),
    url(r'^dashboard/sales_history/$', views.sales_history, name='sales_history'),
]
