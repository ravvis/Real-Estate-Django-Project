from django import forms
from .models import *

class PropertyForm(forms.ModelForm):
    
    class Meta:
        model = Property
        fields = "__all__"