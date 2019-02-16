from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/search/', views.spotify_search, name='search'),
    path('api/vote/', views.vote, name='vote')
]
