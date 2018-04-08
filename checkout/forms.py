from django import forms
# from .models import Order
from django.utils import timezone
from .models import Order

class MakePaymentForm(forms.Form):
  """
  form to collect user payment details. *Sends the details through using
  Stripes own secure channels and the information never actually
  reaches our side of the setup.
  """

  # CHOICES
  MONTH_CHOICES= [(i,i) for i in range(1,12)]
  CURRENT_YEAR = timezone.localtime().year
  YEAR_CHOICES = [(i,i) for i in range(CURRENT_YEAR, CURRENT_YEAR + 10)]

  # extra form fields (not part of the model so not saved in db)
  credit_card_number =  forms.CharField(label='Credit Card Number', required=False)
  cvv = forms.CharField(label="Security Code (CVV)", required=False)
  expiry_month = forms.ChoiceField(label="Month", choices=MONTH_CHOICES, required=False)
  expiry_year = forms.ChoiceField(label="Year", choices=YEAR_CHOICES, required=False)
  stripe_id = forms.CharField(widget=forms.HiddenInput)

class OrderForm(forms.ModelForm):
  class Meta:
    model = Order
    exclude = ('ordered_date', 'total_amount', 'products', 'buyer', 'product_count',)