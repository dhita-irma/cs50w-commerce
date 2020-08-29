from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

from django import forms

from .models import Listing


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('title', placeholder='Enter Listing Title', autocomplete='off'),
                Field('description', placeholder='Listing Description'),
                Field('start_price', placeholder='Set Starting Price'),
                Field('category', placeholder='Select Category'),
                Submit('submit', 'Save Listing', css_class='btn btn-primary float-left'),
                css_class='form-group col-sm-12 col-lg-8 offset-lg-2'
            )
        )

    class Meta:
        model = Listing
        fields = ["title", "description", "start_price", "seller", "category"]
    
        widgets = {
            'title': forms.TextInput,
            'description': forms.Textarea,
            'start_price': forms.TextInput,
            'seller': forms.Select,
            'category': forms.Select
        }
