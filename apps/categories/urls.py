from django.urls import path
from .views import CategoryListView, CategoryCreateView, CategoryUpdateView, CategoryDeleteView

urlpatterns = [
    path('', CategoryListView.as_view(), name='ui_category_list'),
    path('new/', CategoryCreateView.as_view(), name='ui_category_create'),
    path('<int:pk>/edit/', CategoryUpdateView.as_view(), name='ui_category_edit'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='ui_category_delete'),
]
