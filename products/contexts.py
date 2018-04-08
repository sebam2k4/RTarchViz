from django.shortcuts import get_object_or_404
from checkout.models import Order


def owned_assets(request):
  """
  Make cart contents available to all apps and derive some useful data
  to use in cart and other templates
  """
  # retrieve session key for cart and its contents in a dictionary
  orders = Order.objects.filter(buyer_id=request.user.id)
  owned_assets = []
  for order in orders:
    for item in order.products.all():
      owned_assets.append(item)
  print owned_assets
  return {'owned_assets': owned_assets}
