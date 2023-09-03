from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('book/', include('book.urls')),
    path('jjim/', include('jjim.urls')),
    path('api/recommend/', include('recommend.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
