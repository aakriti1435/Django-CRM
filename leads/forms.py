from django import forms

class LeadForm(forms.Form):
    firstName = forms.CharField()
    lastName = forms.CharField()
    age = forms.IntegerField(min_value=0)