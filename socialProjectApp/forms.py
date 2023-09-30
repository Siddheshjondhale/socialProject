from django import forms

class ProfileSearchForm(forms.Form):
  text_input = forms.CharField(
    label='',
    widget=forms.TextInput(attrs={'placeholder': 'Enter username of Instagram', 'id': 'username', 'class': 'centered-input'}),
    required=True
    )

