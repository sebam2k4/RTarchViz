from django import template
from ..models import Product, Review

register = template.Library()

@register.filter
def get_review_count(product):
  count = product.reviews.count()
  if count == 0:
    return 0
  else:
    return '{0}'.format(count)

@register.filter
def get_average_rating(product):
  product_reviews = product.reviews.all()
  count = product_reviews.count()
  if count == 0:
    return 0
  total = 0
  for review in product_reviews:
    total += review.rating
  average_rating = total/ float(count)
  # round up average rating to two decimal places.
  return '{0}'.format(round(average_rating, 2))
  
@register.inclusion_tag('_product_list_cards_partial.html', takes_context=True)
def recent_products(context, num, md=6, lg=4):
  """
  Return the specified number of recent products in a reusable partial
  template. Can optionaly define column width for medium and large
  devices. ALso, make 'request' object available in the template's
  context
  """
  products = Product.objects.all().order_by('-added_date')[:num]
  return {'products': products, 'md': md, 'lg': lg, 'request': context['request']}

@register.inclusion_tag('_product_list_cards_partial.html', takes_context=True)
def user_product_list(context, user, num=None, md=6, lg=4):
  """
  Return the specified number or all user products in a reusable partial
  template. Can optionaly define column width for medium and large
  devices. ALso, accept user object as argument and make 'request' object
  available in the template's context

  Can limit the number of user products to display by providing integer 
  argument for the 'num' parameter. Otherwise all user products will
  be displayed
  """
  if num is None:
    products = Product.objects.filter(seller_id = user.id).order_by('-added_date')
  else:
    products = Product.objects.filter(seller_id = user.id).order_by('-added_date')[:num]
  return {'products': products, 'md': md, 'lg': lg, 'request': context['request']}
