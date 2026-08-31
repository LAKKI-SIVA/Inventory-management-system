from django.urls import path
from .views import (
    ProductListCreateAPIView, 
    ProductRetrieveUpdateDestroyAPIView,
    ProductListView,
    ProductCreateView,
    ProductUpdateView,
    ProductDeleteView,
    ProductDetailView
)

urlpatterns = [
    # ------------------
    # REST API endpoints
    # ------------------
    path('api/', ProductListCreateAPIView.as_view(), name='api_product_list_create'),
    path('api/<int:pk>/', ProductRetrieveUpdateDestroyAPIView.as_view(), name='api_product_detail'),

    # ------------------
    # HTML UI endpoints
    # ------------------
    path('', ProductListView.as_view(), name='ui_product_list'),
    path('new/', ProductCreateView.as_view(), name='ui_product_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='ui_product_detail'),
    path('<int:pk>/edit/', ProductUpdateView.as_view(), name='ui_product_edit'),
    path('<int:pk>/delete/', ProductDeleteView.as_view(), name='ui_product_delete'),
]
