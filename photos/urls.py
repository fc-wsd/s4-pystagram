from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'(?P<pk>[0-9]+)/$', views.view_photo, name='view_photo'),
    url(r'(?P<pk>[0-9]+)/like/$', views.like_photo, name='like_photo'),
    url(
        r'comment/(?P<pk>[0-9]+)/delete$',
        views.delete_comment, name='delete_comment'
    ),
    url(r'^create/$', views.create_photo, name='create_photo'),
]
