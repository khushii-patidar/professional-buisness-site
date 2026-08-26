from django import forms
from .models import Lead


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ['name', 'mobile', 'email', 'requirement']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Your Full Name'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Mobile Number', 'pattern': '[0-9]{10,15}'}),
            'email': forms.EmailInput(attrs={'class': 'form-control custom-input', 'placeholder': 'Email Address'}),
            'requirement': forms.Textarea(attrs={'class': 'form-control custom-input', 'placeholder': 'Describe your requirement...', 'rows': 4}),
        }
