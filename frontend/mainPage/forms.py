from django import forms


    
class AnalysisForm(forms.Form):
    first_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ingrese el primer texto para analizar...'}))
    second_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Ingrese el segundo texto para analizar...'}))