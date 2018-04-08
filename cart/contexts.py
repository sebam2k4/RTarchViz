from django.shortcuts import get_object_or_404
from products.models import Product
from django.contrib import messages


def cart_contents(request):
  """
  Make cart contents available to all apps and derive some useful data
  to use in cart and other templates
  """
  # retrieve session key for cart and its contents in a dictionary
  cart = request.session.get('cart', {})
  cart_items = []

  total = 0
  product_count = 0
  for id in cart:
    product = get_object_or_404(Product, pk=id)
    # get total price
    total += product.price
    # get number of product items in cart
    product_count += 1
    cart_items.append({'id': id, 'product': product})

  return {'cart_items': cart_items, 'total': total, 'product_count': product_count}
