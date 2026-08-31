from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Redirect the root URL (/) to the Products Dashboard so we don't get a 404
    path('', RedirectView.as_view(url='/products/', permanent=False), name='home'),
    
    path('admin/', admin.site.urls),
    # Accounts handles both UI (/accounts/login/) and API (/accounts/api/login/)
    path('accounts/', include('apps.accounts.urls')),
    path('products/', include('apps.products.urls')),
    path('categories/', include('apps.categories.urls')),
    path('customers/', include('apps.customers.urls')),
    path('suppliers/', include('apps.suppliers.urls')),
    path('inventory/', include('apps.inventory.urls')),
    path('orders/', include('apps.orders.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
