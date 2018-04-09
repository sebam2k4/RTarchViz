from django.shortcuts import get_object_or_404
from checkout.models import Order


def owned_assets(request):
  """
  Make user owned(purchased) products available to all apps
  """
  orders = Order.objects.filter(buyer_id=request.user.id)
  owned_assets = []
  for order in orders:
    for item in order.products.all():
      owned_assets.append(item)
  print "owned Assets: {0}".format(owned_assets)
  return {'owned_assets': owned_assets}
