from django.urls import path
from Comics.views import genre_views as views


urlpatterns = [
    path('', views.getGenres, name="genres"),

    path('<str:pk>/', views.getGenre, name="genre"),


]
