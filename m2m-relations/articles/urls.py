from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from articles.views import articles_list

urlpatterns = [
    path('', articles_list, name='articles'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)