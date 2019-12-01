from django import forms


class EmailForm(forms.Form):
    address = forms.CharField(label='Address', max_length=100)
    subject = forms.CharField(label='Subject', max_length=100)
    message = forms.CharField(label='Message', widget=forms.Textarea)
