from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('accounts/', include('user_auth.urls')),
    path('admin/', admin.site.urls)
]
