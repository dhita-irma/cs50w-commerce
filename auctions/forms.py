from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div

from django import forms
from django.utils.translation import gettext_lazy as _

from .models import Listing, Comment, Bid


class ListingForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('title', placeholder='Enter Listing Title', autocomplete='off'),
                Field('description', placeholder='Listing Description'),
                Field('start_price', placeholder='Set Starting Price', autocomplete='off'),
                Field('image_url', placeholder='Enter Image URL'),
                Field('category', placeholder='Select Category'),
                Submit('submit', 'Save Listing', css_class='btn btn-primary float-left'),
                css_class='form-group col-sm-12 col-lg-8 offset-lg-2'
            )
        )

    class Meta:
        model = Listing
        fields = ("title", "description", "start_price", "category", "image_url")
        exclude = ["seller", "created_date"]

        labels = {
            'start_price': _('Starting Price'),
            'category': _('Category (Optional)'),
            'img_url': _('Image URL'),

        }


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('body', placeholder='Enter your comment here'),
                Submit('submit', 'Send', css_class='btn btn-primary float-left'),
                css_class='form-group col-sm-12 col-lg-12'
            )
        )
    
    class Meta:
        model = Comment
        fields = ('body',)
        exclude = ['listing ', 'user', 'posted_date']

        labels = {
            'body': _('Comment'),
        }

class BidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Div(
                Field('price', css_class='form-group mx-sm-3 mb-2'),
                Submit('submit', 'Place Bid', css_class='btn btn-primary float-left mb-2'),
                css_class='form-inline'
            )
        )
    
    class Meta:
        model = Bid
        fields = ('price',)
        exclude = ['listing ', 'user', 'time']

        labels = {
            'price': _('Bid')
        }