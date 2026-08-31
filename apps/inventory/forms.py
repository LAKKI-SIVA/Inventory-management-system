from django import forms
from .models import StockTransaction

class StockAdjustmentForm(forms.Form):
    """
    Standard HTML Form for stock adjustments.
    Notice we are using forms.Form instead of forms.ModelForm because
    we don't want to save a model directly; we want to pass this data to our Service.
    """
    transaction_type = forms.ChoiceField(choices=StockTransaction.TransactionType.choices)
    quantity = forms.IntegerField(help_text="Use negative numbers to remove stock")
    reference_number = forms.CharField(max_length=100, required=False)
    notes = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
