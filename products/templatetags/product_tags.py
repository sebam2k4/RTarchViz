from django import template
from ..models import Product

register = template.Library()


@register.inclusion_tag('_product_list_cards_partial.html', takes_context=True)
def home_recent_products(context, num, md=6, lg=4):
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
  devices. ALso, pass user object as argument and make 'request' object
  available in the template's context
  """
  if num is None:
    products = Product.objects.filter(seller_id = user.id).order_by('-added_date')
  else:
    products = Product.objects.filter(seller_id = user.id).order_by('-added_date')[:num]
  return {'products': products, 'md': md, 'lg': lg, 'request': context['request']}


# ALTERNATE INLCUSION TAG WITH DIFFERENT TEMPLATE - MAY USE INSTEAD OF THE ONE ABOVE
# @register.inclusion_tag('_user_product_list_partial.html')
# def user_product_list(user, num=None):
#   """
#   Return the specified number of recent products in a reusable partial
#   template. Can optionaly define column width for medium and large
#   devices. ALso, make 'request' object available in the context
#   """
#   if num is None:
#     products = Product.objects.filter(seller_id = user.id).order_by('-added_date')
#   else:
#     products = Product.objects.filter(seller_id = user.id).order_by('-added_date')[:num]
#   return {'products': products}