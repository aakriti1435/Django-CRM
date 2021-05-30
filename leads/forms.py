from django import forms
from .models import Lead

class LeadForm(forms.Form):
    firstName = forms.CharField()
    lastName = forms.CharField()
    age = forms.IntegerField(min_value=0)


class LeadModelForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = (
            'firstName','lastName','age','agent'
        )