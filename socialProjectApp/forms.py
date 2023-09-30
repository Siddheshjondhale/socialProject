from django import forms

class ProfileSearchForm(forms.Form):
    social_media_choices = [
        ('instagram', 'Instagram'),
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
    ]
    
    social_media = forms.ChoiceField(
        choices=social_media_choices,
        label='',
        widget=forms.Select(attrs={'style': 'padding: 5px; border-radius: 10px;'})
    )
    
    username = forms.CharField(
        max_length=100,
        label='',
        widget=forms.TextInput(attrs={'placeholder': 'Enter username', 'style': 'padding: 5px; border-radius: 10px; width: 300px;'})
    )
