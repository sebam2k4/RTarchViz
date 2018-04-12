from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.page1, name='page1'),
]