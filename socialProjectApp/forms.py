from django import forms

class ProfileSearchForm(forms.Form):
    text_input = forms.CharField(
        label='Enter Text',
        widget=forms.TextInput(attrs={'placeholder': 'Enter text here','id':'username'}),
        required=True
    )
