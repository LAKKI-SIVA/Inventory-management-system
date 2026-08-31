from django.urls import path
from .views import (
    OrderListAPIView, OrderCreateAPIView, OrderProcessAPIView,
    OrderListView, OrderDetailView, OrderCreateView, OrderProcessView
)

urlpatterns = [
    # ------------------
    # REST API ROUTES
    # ------------------
    path('api/', OrderListAPIView.as_view(), name='api_order_list'),
    path('api/create/', OrderCreateAPIView.as_view(), name='api_order_create'),
    path('api/<int:pk>/process/', OrderProcessAPIView.as_view(), name='api_order_process'),
    
    # ------------------
    # HTML UI ROUTES
    # ------------------
    path('', OrderListView.as_view(), name='ui_order_list'),
    path('new/', OrderCreateView.as_view(), name='ui_order_create'),
    path('<int:pk>/', OrderDetailView.as_view(), name='ui_order_detail'),
    path('<int:pk>/process/', OrderProcessView.as_view(), name='ui_order_process'),
]
