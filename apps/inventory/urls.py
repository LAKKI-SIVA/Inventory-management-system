from django.urls import path
from .views import (
    StockListAPIView, StockAdjustAPIView,
    InventoryDashboardView, StockAdjustView,
    StockTransactionListView
)

urlpatterns = [
    # ------------------
    # REST API ROUTES
    # ------------------
    path('api/stock/', StockListAPIView.as_view(), name='api_stock_list'),
    path('api/stock/<int:pk>/adjust/', StockAdjustAPIView.as_view(), name='api_stock_adjust'),
    
    # ------------------
    # HTML UI ROUTES
    # ------------------
    path('', InventoryDashboardView.as_view(), name='ui_inventory_dashboard'),
    path('<int:pk>/adjust/', StockAdjustView.as_view(), name='ui_stock_adjust'),
    path('transactions/', StockTransactionListView.as_view(), name='ui_inventory_transactions'),
]
