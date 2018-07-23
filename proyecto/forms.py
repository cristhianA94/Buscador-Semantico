from django import forms

class SparqlForm(forms.Form):
    query = forms.CharField(label='', max_length=100,required=True,widget=forms.TextInput(
        attrs={
        'class':'form-control',
        'placeholder':'Qué estás buscando?'
        }))
    # post = forms.CharField(widget=forms.Textarea(            attrs={
    #             'class':'form-control',
    #         }),required=True,label='')

class UriForm(forms.Form):
    uri = forms.CharField(label='', max_length=150,required=True,widget=forms.TextInput(
            attrs={
            'class':'form-control',
            'placeholder':'Ingrese una uri'
            }))
