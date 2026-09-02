from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Product
from .forms import ProductForm
from .services import ProductService

# ---------------------------------------------------------
# HTML UI VIEWS (No JS)
# ---------------------------------------------------------

class ProductListView(LoginRequiredMixin, ListView):
    """
    Renders the HTML page listing all products.
    """
    model = Product
    template_name = 'products/list.html'
    context_object_name = 'products'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Product.objects.select_related('category', 'supplier').all().order_by('-id')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        return queryset


class ProductCreateView(LoginRequiredMixin, CreateView):
    """
    Renders the HTML form and handles standard POST submissions to create a product.
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('ui_product_list')

    def form_valid(self, form):
        # We intercept the valid form data to use our Service Layer!
        try:
            ProductService.create_product(
                sku=form.cleaned_data['sku'],
                name=form.cleaned_data['name'],
                unit_price=form.cleaned_data['unit_price'],
                category_id=form.cleaned_data['category'].id,
                supplier_id=form.cleaned_data['supplier'].id if form.cleaned_data.get('supplier') else None,
                description=form.cleaned_data.get('description', ''),
                status=form.cleaned_data.get('status', Product.Status.DRAFT)
            )
            messages.success(self.request, "Product created successfully!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)


class ProductDetailView(LoginRequiredMixin, DetailView):
    """
    Renders the HTML page showing a single product's details.
    """
    model = Product
    template_name = 'products/detail.html'
    context_object_name = 'product'

class ProductUpdateView(LoginRequiredMixin, UpdateView):
    """
    Renders the HTML form and handles standard POST submissions to update a product.
    """
    model = Product
    form_class = ProductForm
    template_name = 'products/form.html'
    success_url = reverse_lazy('ui_product_list')

    def form_valid(self, form):
        # Using Service Layer
        try:
            ProductService.update_product(
                product=self.get_object(),
                sku=form.cleaned_data['sku'],
                name=form.cleaned_data['name'],
                unit_price=form.cleaned_data['unit_price'],
                category_id=form.cleaned_data['category'].id,
                supplier_id=form.cleaned_data['supplier'].id if form.cleaned_data.get('supplier') else None,
                description=form.cleaned_data.get('description', ''),
                status=form.cleaned_data.get('status', Product.Status.DRAFT)
            )
            messages.success(self.request, "Product updated successfully!")
            return super().form_valid(form)
        except Exception as e:
            messages.error(self.request, str(e))
            return self.form_invalid(form)

class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'products/delete_confirm.html'
    success_url = reverse_lazy('ui_product_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Product deleted successfully!")
        return super().delete(request, *args, **kwargs)
