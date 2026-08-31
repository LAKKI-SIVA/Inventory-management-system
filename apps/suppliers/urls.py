from django.urls import path
from .views import SupplierListView, SupplierCreateView, SupplierUpdateView, SupplierDeleteView

urlpatterns = [
    path('', SupplierListView.as_view(), name='ui_supplier_list'),
    path('new/', SupplierCreateView.as_view(), name='ui_supplier_create'),
    path('<int:pk>/edit/', SupplierUpdateView.as_view(), name='ui_supplier_edit'),
    path('<int:pk>/delete/', SupplierDeleteView.as_view(), name='ui_supplier_delete'),
]
