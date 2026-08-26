from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "Lokeshh Ai Tools — Admin"
admin.site.site_title = "Lokeshh Admin"
admin.site.index_title = "Welcome Lokeshh! Manage Your Portfolio"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('portfolio.api_urls')),
    path('', include('portfolio.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
