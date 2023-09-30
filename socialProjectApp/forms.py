from django import forms

class ProfileSearchForm(forms.Form):
    url = forms.URLField(
        label='Enter Profile URL',
        widget=forms.URLInput(attrs={'placeholder': 'https://www.example.com/user_profile'}),
        required=True
    )
