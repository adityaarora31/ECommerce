from django import forms


class ContactQueryForm(forms.Form):

    name = forms.CharField(max_length=60),
    email = forms.EmailField(max_length=50),
    subject = forms.CharField(max_length=30),
    query = forms.Textarea()
