from django import forms
# from .models import Order
from django.utils import timezone
from .models import Order


class MakePaymentForm(forms.Form):
    """
    form to collect user payment details. Sends the details through using
    Stripes own secure channels and the information never actually
    reaches our servers.
    """

    # CHOICES
    MONTH_CHOICES = [(i, i) for i in range(1, 13)]
    CURRENT_YEAR = timezone.localtime().year
    YEAR_CHOICES = [(i, i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 11)]

    # extra form fields (not part of the model so not saved in db)
    credit_card_number = forms.CharField(
        label='Credit Card Number',
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': 'Long number from the front of your card'})
        )

    cvv = forms.CharField(
        label="Security Code (CVV)",
        required=False,
        widget=forms.TextInput(
            attrs={'placeholder': '3 digit security number from the back'})
        )

    expiry_month = forms.ChoiceField(
        label="Card Expiration Month",
        choices=MONTH_CHOICES,
        required=False)

    expiry_year = forms.ChoiceField(
        label="Card Expiration Year",
        choices=YEAR_CHOICES, required=False)
        
    stripe_id = forms.CharField(widget=forms.HiddenInput)
