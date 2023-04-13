from django.urls import path
from Comics.views import comic_views as views


urlpatterns = [
    path('', views.getComics, name="comics"),
    path('create/', views.createComic, name="comic-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path('scraper/', views.crawl, name='scraper'),
    path('top/', views.getTopComics, name="comicsTop"),
    path('<str:pk>/', views.getComic, name="comic"),
    path('update/<str:pk>/', views.updateComic, name='comic-update'),
    path('delete/<str:pk>/', views.deleteComic, name='comic-delete'),

]
