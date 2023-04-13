from django.urls import path
from Comics.views import category_views as views


urlpatterns = [
    path('', views.getCategorys, name="categorys"),

    path('<str:pk>/', views.getCategory, name="category"),


]
