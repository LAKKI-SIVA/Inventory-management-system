from django import forms
from .models import Supplier

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'contact_name', 'email', 'phone', 'address', 'is_active']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'contact_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Primary Contact Person'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'contact@company.com'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+1 (555) 123-4567'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Full address', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-checkbox'})
        }
