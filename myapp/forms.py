from django import forms

class BookForm(forms.Form):
    title = forms.CharField(label='Title')
    price = forms.FloatField(label='Price')
    pub_date = forms.DateTimeField(
        input_formats = ['%Y-%m-%dT%H:%M'],
        widget = forms.DateTimeInput(
            attrs={'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M')
    )
    publisher = forms.IntegerField(label='Publisher')

class PublisherForm(forms.Form):
    publisher_name = forms.CharField(label='Publisher')
    location = forms.CharField(label='Location')
