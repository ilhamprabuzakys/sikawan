from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    #path("__debug__/", include("debug_toolbar.urls")),
    path('admin/', admin.site.urls),
    # path("__reload__/", include("django_browser_reload.urls")), # HOT RELOAD
    
    # Guest section
    path('', include('home.urls')),
    
    # Authentication section
    path('accounts/', include('accounts.urls')),

    # Dashboard section
    path('dashboard/', include('dashboard.urls')),
    path('dashboard/masters/', include('masters.urls')),
    path('dashboard/users/', include('users.urls')),
    path('dashboard/literasi/', include('literasi.urls')),

]

admin.site.site_header = 'Kawasan Rawan'
admin.site.index_title = 'Kelola data Kawasan Rawan'

handler404 = "home.views.handler_404"
handler500 = "home.views.handler_500"

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
