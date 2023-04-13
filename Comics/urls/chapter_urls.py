from django.urls import path
from Comics.views import chapter_views as views

urlpatterns = [
    path('create/', views.createChapter, name='createchapter'),
    path('', views.getChapters, name="chapters"),
    path('<str:pk>/', views.getChapter, name="chapter"),
    path('edit/<str:pk>/', views.updateChapter, name='editchapter'),
    path('delete/<str:pk>/', views.deleteChapter, name='deletechapter'),
    path('<str:pk>/reviews/', views.createChapterReview, name="create-review"),
]
