from django import template
from ..models import PurchaseHistory

register = template.Library()

@register.simple_tag
def get_total_for_sold_product(product):
  """ 
  total for product sold derived from PurchaseHistory for keeping
  accurate totals.
  """
  total = 0
  items = PurchaseHistory.objects.filter(product_id=product.id)
  for item in items:
    total += item.product_price
  return total

@register.simple_tag
def get_account_balance(user):
  """
  total from all sales
  """
  total = 0
  all_sales = PurchaseHistory.objects.filter(seller_id=user.id)
  for sales in all_sales:
    total += sales.product_price
  return total