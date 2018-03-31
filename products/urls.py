from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.products_list, name="products_list"),
    url(r'^new/$', views.new_product, name="new_product"),
    url(r'^(?P<slug>[-\w]+)--(?P<id>\d+)/?$', views.product_detail, name='product_detail'),
    url(r'^(?P<slug>[-\w]+)--(?P<id>\d+)/edit/$', views.edit_product, name='edit_product'),
    url(r'^(?P<slug>[-\w]+)--(?P<id>\d+)/delete/$', views.delete_product, name='delete_product'),
]