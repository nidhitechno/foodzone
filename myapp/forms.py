from django import forms
from .models import TableBooking

class BookingForm(forms.ModelForm):
    class Meta:
        model = TableBooking
        fields = ['name', 'email', 'mobile', 'date', 'time', 'guests']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'mobile': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'guests': forms.NumberInput(attrs={'class': 'form-control'}),
        }
