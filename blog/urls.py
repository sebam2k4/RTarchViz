from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.posts_list, name="posts_list")
]