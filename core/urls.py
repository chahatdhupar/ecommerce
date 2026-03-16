from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# customize admin panel titles
admin.site.site_header = 'ShopNow Admin'
admin.site.site_title = 'ShopNow Admin Portal'
admin.site.index_title = 'Welcome to ShopNow Admin Panel'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls')),
    path('users/', include('users.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)