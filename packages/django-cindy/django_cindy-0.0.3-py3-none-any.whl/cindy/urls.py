from django.urls import path

from . import views

urlpatterns = [
    path('feed/<int:feed_id>/original', views.FeedView(), name='feed'),
]
