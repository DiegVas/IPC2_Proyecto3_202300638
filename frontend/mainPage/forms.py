from django import forms

class XMLUploadForm(forms.Form):
    xml_file = forms.FileField(
        label='Selecciona un archivo XML',
        help_text='Archivo XML con mensajes para análisis',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.xml'
        })
    )