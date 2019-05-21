from django import forms


class UserEmailForm(forms.Form):
    email = forms.EmailField(max_length=50)
