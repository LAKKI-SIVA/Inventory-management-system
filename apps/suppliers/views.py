from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import redirect
from .models import Supplier
from .forms import SupplierForm

class SupplierListView(LoginRequiredMixin, ListView):
    model = Supplier
    template_name = 'suppliers/list.html'
    context_object_name = 'suppliers'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Supplier.objects.all().order_by('name')
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)
        return queryset

class SupplierCreateView(LoginRequiredMixin, CreateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/form.html'
    success_url = reverse_lazy('ui_supplier_list')

    def form_valid(self, form):
        messages.success(self.request, "Supplier created successfully!")
        return super().form_valid(form)

class SupplierUpdateView(LoginRequiredMixin, UpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name = 'suppliers/form.html'
    success_url = reverse_lazy('ui_supplier_list')

    def form_valid(self, form):
        messages.success(self.request, "Supplier updated successfully!")
        return super().form_valid(form)

class SupplierDeleteView(LoginRequiredMixin, DeleteView):
    model = Supplier
    template_name = 'suppliers/delete_confirm.html'
    success_url = reverse_lazy('ui_supplier_list')

    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            messages.success(self.request, "Supplier deleted successfully!")
            return response
        except ProtectedError:
            messages.error(request, "Cannot delete this supplier because it has products assigned to it.")
            return redirect(self.success_url)
