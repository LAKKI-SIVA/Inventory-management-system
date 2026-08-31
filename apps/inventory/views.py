from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect

from .models import Stock, StockTransaction
from .serializers import StockSerializer, StockAdjustSerializer
from .services import InventoryService
from .forms import StockAdjustmentForm

# ---------------------------------------------------------
# REST API VIEWS
# ---------------------------------------------------------

class StockListAPIView(generics.ListAPIView):
    """API endpoint to view all stock levels."""
    queryset = Stock.objects.select_related('product').all()
    serializer_class = StockSerializer
    permission_classes = (IsAuthenticated,)

class StockAdjustAPIView(APIView):
    """API endpoint to adjust stock."""
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        serializer = StockAdjustSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                InventoryService.adjust_stock(
                    stock=stock,
                    quantity_change=serializer.validated_data['quantity'],
                    transaction_type=serializer.validated_data['transaction_type'],
                    user=request.user,
                    reference_number=serializer.validated_data.get('reference_number', ''),
                    notes=serializer.validated_data.get('notes', '')
                )
                return Response({"status": "Stock adjusted successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# HTML UI VIEWS (No JS)
# ---------------------------------------------------------

class InventoryDashboardView(LoginRequiredMixin, ListView):
    """HTML Dashboard for Inventory."""
    model = Stock
    template_name = 'inventory/dashboard.html'
    context_object_name = 'stocks'
    
    def get_queryset(self):
        return Stock.objects.select_related('product').all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from apps.products.models import Product
        from apps.orders.models import Order
        from apps.customers.models import Customer
        from django.db.models import Sum, F
        
        # Top KPI Cards
        context['total_products'] = Product.objects.count()
        context['total_stock'] = Stock.objects.aggregate(total=Sum('quantity'))['total'] or 0
        context['total_orders'] = Order.objects.count()
        context['total_customers'] = Customer.objects.count()
        
        # Stock overview (mocked data points for SVG line chart)
        context['stock_history'] = [
            {'date': 'May 20', 'value': 5200},
            {'date': 'May 27', 'value': 5000},
            {'date': 'Jun 03', 'value': 5800},
            {'date': 'Jun 10', 'value': 6200},
            {'date': 'Jun 17', 'value': 7500},
            {'date': 'Jun 20', 'value': 8653},
        ]
        
        # Low Stock Alert
        context['low_stock_items'] = Stock.objects.filter(quantity__lte=F('reorder_level')).select_related('product')[:5]
        
        # Recent Orders
        context['recent_orders'] = Order.objects.select_related('customer').order_by('-created_at')[:5]
        
        # Top Selling Products (Placeholder since no historical sales table exists yet)
        context['top_products'] = Product.objects.all()[:5]
        
        return context

class StockAdjustView(LoginRequiredMixin, FormView):
    """HTML Form View for adjusting stock."""
    template_name = 'inventory/stock_adjust.html'
    form_class = StockAdjustmentForm
    success_url = reverse_lazy('ui_inventory_dashboard')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['stock'] = get_object_or_404(Stock, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        stock = get_object_or_404(Stock, pk=self.kwargs['pk'])
        try:
            InventoryService.adjust_stock(
                stock=stock,
                quantity_change=form.cleaned_data['quantity'],
                transaction_type=form.cleaned_data['transaction_type'],
                user=self.request.user,
                reference_number=form.cleaned_data.get('reference_number', ''),
                notes=form.cleaned_data.get('notes', '')
            )
            messages.success(self.request, f"Stock for {stock.product.name} updated successfully.")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class StockTransactionListView(LoginRequiredMixin, ListView):
    model = StockTransaction
    template_name = 'inventory/transactions.html'
    context_object_name = 'transactions'
    paginate_by = 15

    def get_queryset(self):
        return StockTransaction.objects.select_related('stock__product', 'created_by').all().order_by('-created_at')
