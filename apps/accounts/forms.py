from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()

class UserUIRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth-form-control', 'placeholder': 'Create a password'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'auth-form-control', 'placeholder': 'Confirm your password'}))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'auth-form-control', 'placeholder': 'Enter your full name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'auth-form-control', 'placeholder': 'Enter your email'}))

    class Meta:
        model = User
        fields = ['first_name', 'email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(username=email).exists():
            raise ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match!")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use email as username if username is required
        user.username = self.cleaned_data['email']
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
