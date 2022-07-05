from django import forms

class BookForm(forms.Form):
    title = forms.CharField(label='Title')
    price = forms.FloatField(label='Price')
    pub_date = forms.DateTimeField(label='Publish Date')
    publisher = forms.IntegerField(label='Publisher')

class PublisherForm(forms.Form):
    publisher_name = forms.CharField(label='Publisher')
    location = forms.CharField(label='Location')
