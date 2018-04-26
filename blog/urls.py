from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.posts_list, name="posts_list"),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/?$',
        views.post_detail,
        name='post_detail'),
]