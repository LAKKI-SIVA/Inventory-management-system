from django.urls import path
from .views import CustomerListView, CustomerCreateView, CustomerUpdateView, CustomerDeleteView

urlpatterns = [
    path('', CustomerListView.as_view(), name='ui_customer_list'),
    path('new/', CustomerCreateView.as_view(), name='ui_customer_create'),
    path('<int:pk>/edit/', CustomerUpdateView.as_view(), name='ui_customer_edit'),
    path('<int:pk>/delete/', CustomerDeleteView.as_view(), name='ui_customer_delete'),
]
