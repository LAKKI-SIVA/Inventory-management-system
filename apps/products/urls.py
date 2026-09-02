from django.urls import path
from .views import (
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView
)

urlpatterns = [
    # HTML UI endpoints
    # ------------------
    path('', ProductListView.as_view(), name='ui_product_list'),
    path('new/', ProductCreateView.as_view(), name='ui_product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='ui_product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='ui_product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='ui_product_delete'),
]
