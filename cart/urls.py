from django.conf.urls import url, include
import views


urlpatterns = [
    url(r'^$', views.view_cart, name='view_cart'),
    url(r'^add/(?P<product_id>\d+)', views.add_to_cart, name='add_to_cart'),
    url(r'^clear/$', views.clear_cart, name='clear_cart'),
    url(r'^adjust/(?P<product_id>\d+)', views.remove_cart_item, name='remove_cart_item'),
]
