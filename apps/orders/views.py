from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Order
from .serializers import OrderSerializer, OrderCreateSerializer
from .services import OrderService
from .forms import OrderForm, OrderItemFormSet
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, View

class OrderListAPIView(generics.ListAPIView):
    """
    Returns a list of all orders.
    """
    queryset = Order.objects.select_related('customer').prefetch_related('items__product').all()
    serializer_class = OrderSerializer
    permission_classes = (IsAuthenticated,)


class OrderCreateAPIView(APIView):
    """
    API endpoint to place a new order.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            try:
                order = OrderService.create_order(
                    customer_id=serializer.validated_data['customer_id'],
                    items_data=serializer.validated_data['items'],
                    notes=serializer.validated_data.get('notes', '')
                )
                
                # Return the fully created order using the read serializer
                response_serializer = OrderSerializer(order)
                return Response(response_serializer.data, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                # If InventoryService fails (e.g., negative stock), it catches here!
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
                
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderProcessAPIView(APIView):
    """
    API endpoint to mark an order as SHIPPED.
    """
    permission_classes = (IsAuthenticated,)

    def post(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
            OrderService.process_order(order, user=request.user)
            return Response({"status": "Order processed and shipped successfully."}, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ---------------------------------------------------------
# HTML UI VIEWS (No JS)
# ---------------------------------------------------------

class OrderListView(LoginRequiredMixin, ListView):
    """
    HTML Dashboard for Orders.
    """
    model = Order
    template_name = 'orders/list.html'
    context_object_name = 'orders'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Order.objects.select_related('customer').all().order_by('-created_at')
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class OrderDetailView(LoginRequiredMixin, DetailView):
    """
    HTML View for seeing a specific order and its items.
    """
    model = Order
    template_name = 'orders/detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        # Prefetch the items and their related products to prevent N+1 queries!
        return Order.objects.select_related('customer').prefetch_related('items__product').all()


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'orders/form.html'
    
    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.POST:
            data['items'] = OrderItemFormSet(self.request.POST)
        else:
            data['items'] = OrderItemFormSet()
        return data
        
    def form_valid(self, form):
        context = self.get_context_data()
        items = context['items']
        
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.total_amount = 0 # Will be calculated by service
            self.object.save()
            
            if items.is_valid():
                items.instance = self.object
                items.save()
                
                # Recalculate total amount using the actual items
                items_data = [{'product_id': item.product.id, 'quantity': item.quantity} for item in self.object.items.all()]
                
                try:
                    # We re-route to the service layer for calculations and creation
                    # We just need to update total_amount here.
                    self.object.total_amount = sum([item.product.price * item.quantity for item in self.object.items.all()])
                    self.object.save()
                    messages.success(self.request, "Order created successfully.")
                except Exception as e:
                    messages.error(self.request, str(e))
                    return self.form_invalid(form)
            else:
                return self.render_to_response(self.get_context_data(form=form))
                
        from django.urls import reverse
        return redirect(reverse('ui_order_detail', kwargs={'pk': self.object.pk}))


class OrderProcessView(LoginRequiredMixin, View):
    def post(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        try:
            OrderService.process_order(order, user=request.user)
            messages.success(request, f"Order #{order.id} has been processed and shipped.")
        except Exception as e:
            messages.error(request, f"Error processing order: {str(e)}")
        
        from django.urls import reverse
        return redirect(reverse('ui_order_detail', kwargs={'pk': order.id}))
