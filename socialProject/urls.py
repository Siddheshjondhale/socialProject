
from django.contrib import admin
from django.urls import path,include
from django.conf.urls.static import static

from socialProject import settings

 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('socialProjectApp.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
