from django.contrib import admin
from django.urls import path, include

from expense_track_main import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('expenses/', include('expense_app.urls')),
    path('budget/', include('budget_app.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('settings/', include('usersettings.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)