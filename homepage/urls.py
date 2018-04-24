from django.conf.urls import url
import views

urlpatterns = [
    url(r'^$', views.homepage, name='homepage'),
    url(r'^newsletter_signup/$', views.newsletter_signup, name='newsletter_signup'),
]
