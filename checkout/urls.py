from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.checkout, name='checkout'),
    url(r'^thank_you/$', views.thank_you, name='thank_you'),
]
