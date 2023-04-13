from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html')),
    path('api/comics/',  include('Comics.urls.comic_urls')),
    path('api/users/',  include('Comics.urls.user_urls')),
    path('api/chapters/',  include('Comics.urls.chapter_urls')),
    path('api/genres/',  include('Comics.urls.genre_urls')),
    path('api/categorys/',  include('Comics.urls.category_urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
