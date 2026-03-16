from django import forms
from .models import LostItem, FoundItem

class LostItemForm(forms.ModelForm):
    class Meta:
        model = LostItem
        fields = ['name', 'description', 'category', 'image', 'location', 'date_item']
        widgets = {
            'date_item': forms.DateInput(attrs={'type': 'date'}),
        }

class FoundItemForm(forms.ModelForm):
    class Meta:
        model = FoundItem
        fields = ['name', 'description', 'category', 'image', 'location', 'date_item']
        widgets = {
            'date_item': forms.DateInput(attrs={'type': 'date'}),
        }
