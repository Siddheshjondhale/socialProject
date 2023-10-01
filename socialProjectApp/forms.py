from django import forms

class ProfileSearchForm(forms.Form):
    text_input = forms.CharField(
        label='',
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter username of Instagram',
            'id': 'username',
            'class': 'centered-input',
            'style': 'border: none; outline: none;'  # Remove border and outline
        }),
        required=False  
    )
    csv_file = forms.FileField(label='', required=False)
