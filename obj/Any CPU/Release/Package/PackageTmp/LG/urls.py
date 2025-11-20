from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

# Redirect root URL to login if user is not authenticated, else go to home
def redirect_to_login_or_home(request):
    if request.user.is_authenticated:
        return redirect("home")  # If logged in, go to home
    return redirect("login")  # Otherwise, go to login

urlpatterns = [
    path('', redirect_to_login_or_home, name='root_redirect'),  # Root URL redirects dynamically
    path('admin/', admin.site.urls),
    path('master/', include('master.urls')),  # Include your app URLs
    path('raw_material/', include('raw_material.urls')), 
    path('packing_materials/', include('packing_materials.urls')),
    path('reports/', include('reports.urls')),
    path('finished_goods/', include('finished_goods.urls')),
    path('asset_management/', include('asset_management.urls')),
    path('Administrator_settings/', include('Administrator_settings.urls')),
    path('stock_statement/', include('stock_statement.urls')),
    path('dashboard/', include('dashboard.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
