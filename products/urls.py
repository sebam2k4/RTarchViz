from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.products_list, name="products_list"),
    url(r'^(?P<slug>[-\w]+)--(?P<id>\d+)/?$', views.product_detail, name='product_detail'),
]