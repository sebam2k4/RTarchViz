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

