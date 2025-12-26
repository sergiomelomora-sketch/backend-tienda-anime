#HECHO POR EL EQUIPO
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from appTienda.api.router import router_insumo

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/', include(router_insumo.urls)),
    
    path('', include('appTienda.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
