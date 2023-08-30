from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/user/', include('user.urls')),
    path('book/', include('book.urls')),
    path('jjim/', include('jjim.urls')),
]
