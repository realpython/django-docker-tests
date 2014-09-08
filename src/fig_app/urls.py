from django.conf.urls import patterns, url
from fig_app import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
)
