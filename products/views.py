# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import Product, Review
from .forms import ProductForm, ReviewForm


def products_list(request):
  """
  This view does three things:

  1. Provides filtering by category and various ordering choices
  to user through 2 select fields in the template: When user selects
  an option, a get request is made with the user's choice as a query
  string and is matched with one of the predefined options below to
  apply the appropriate filter to the queryset.

  2. Paginates the list of post objects, filtered or not.

  3. returns paginated list of products and
  renders them to the 'products_list.html' template. 

  This view is dealing with up to three query strings at the same
  time, one for pagination '?page=' and the other two for selecting
  category & sorting '?product-category-select=''&product-sort-select'.
  To avoid the category and sorting query strings from being cleared,
  by requesting next page of results with paginator, the form's
  select options in the template have to be matched with user selected
  options and set 'selected' attribute on the specified option tags.
  """
  products = Product.objects.all()

  # define filter choices and get filtered objects based on user select
  # note: refactor this code as it pretty much uses all hard coded
  #       values. See if can fill a tuple from list of the actual
  #       available categories? This would be useful for when categories
  #       are added or modified.
  category_choices = ('all products', 'assets', 'environment', 'blueprint', 'materials')
  sort_choices = ('newest', 'oldest', 'most popular', 'a-z', 'z-a')

  if request.method == 'GET':
    chosen_category = request.GET.get('product-category-select')
    chosen_sort = request.GET.get('product-sort-select')
    
    if chosen_category:
      if chosen_category == 'all products':
        products_by_category = products
      else:
        products_by_category = products.filter(category=chosen_category)

    if chosen_sort:
      if chosen_sort == 'newest':
        products_by_sort = products_by_category.order_by('-added_date')
      elif chosen_sort == 'oldest':
        products_by_sort  = products_by_category.order_by('added_date')
      elif chosen_sort == 'most popular':
        products_by_sort = products_by_category.order_by('-sold_count')
      elif chosen_sort == 'a-z':
        products_by_sort = products_by_category.order_by('name')
      elif chosen_sort == 'z-a':
        products_by_sort = products_by_category.order_by('-name')
      products = products_by_sort

  # paginate the products list
  paginator = Paginator(products, 9)
  products_page = request.GET.get('page')
  try:
    products = paginator.page(products_page)
  except PageNotAnInteger:
    # if page is not an integer, deliver first page
    products = paginator.page(1)
  except EmptyPage:
    # deliver last page of results when page is out of range
    products = paginator.page(paginator.num_pages)

  context = {'products': products, 'category_choices': category_choices,
             'sort_choices': sort_choices, 'chosen_sort': chosen_sort,
             'chosen_category': chosen_category, 'paginator': paginator}
  return render(request, 'products_list.html', context)

def product_detail(request, slug, id):
  """
  A view that returns a single product object based on product's
  slug and id and its user reviews and renders it to the
  'product_detail.html' template. Or return a 404 error if the product
  is not found. Also, handles creating new user reviews using the
  ReviewForm and rendering it in a partial template
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  product_reviews = product.reviews.all()
  #product_reviews = Review.objects.filter(product_id=product.id)
  
  # save the url user came from. Will include any GET parameters and
  # hence preserve any user applied list filters and ordering.
  previous_page = request.META.get('HTTP_REFERER')
  print previous_page
  # clock up the number of product views
  product.view_count += 1
  product.save()
  # load product review form
  form = ReviewForm()

  # check if user already reviewed. Only 1 review/product allowed
  already_reviewed = False
  if product_reviews.filter(buyer_id=request.user.id).count() >= 1:
    already_reviewed = True
  
  # Review Form
  form_action = Product.get_absolute_url(product)
  form_button = "Add Review"
  if request.method == "POST":
    form = ReviewForm(request.POST)
    if form.is_valid():
      review = form.save(commit=False)
      review.buyer = request.user
      review.product = product
      review.save()
      messages.success(request, 'You have successfully added a product review')
      # redirect to the new product after save
      return redirect(Product.get_absolute_url(product))

  context = {"product": product, "product_reviews": product_reviews,
             "previous_page": previous_page, "form": form, "already_reviewed": already_reviewed,
             "form_action": form_action, "form_button": form_button }

  return render(request, "product_detail.html", context)

@login_required
def new_product(request):
  """
  A view for creatubg a new product
  """
  if request.method == "POST":
    form = ProductForm(request.POST, request.FILES)
    if form.is_valid():
      product = form.save(commit=False)
      product.seller = request.user
      product.save()
      messages.success(request, 'You have successfully created a new product')
      # redirect to the new product after save
      return redirect(Product.get_absolute_url(product))
  else:
    form = ProductForm()

  context = {'form': form}
  return render(request, 'product_form_new.html', context)

@login_required
def edit_product(request, slug, id):
  """
  A view for editing user's existing product
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  # make sure user is the product owner
  if request.user.id == product.seller_id:
    if request.method == "POST":
      # Create instance of ProductForm & bind file data and form data
      form = ProductForm(request.POST, request.FILES, instance=product)
      if form.is_valid():
        product = form.save(commit=False)
        product.seller = request.user
        product.save()
        messages.success(request, 'You have successfully updated your product')
        return redirect(Product.get_absolute_url(product))
    else:
      # Render the edited product
      form = ProductForm(instance=product)

    context = {'form': form}
    return render(request, 'product_form_edit.html', context)
  else:
    # if not product owner, raise 403 forbidden exception and render
    # 403.html template
    messages.error(request, 'You cannot edit this product')
    raise PermissionDenied

@login_required
def delete_product(request, slug, id):
  """
  A view that handles deleting user's existing product
  """
  product = get_object_or_404(Product, slug=slug, pk=id)
  # make sure user is the product owner
  if request.user.id == product.seller_id:
    product.delete()
    messages.success(request, 'You have successfully deleted your product')
    return redirect('dashboard')
  else:
    # if not product owner, raise 403 forbidden exception and render
    #  403.html template
    messages.error(request, 'You cannot delete this product')
    raise PermissionDenied

@login_required
def edit_review(request, product_slug, product_id, review_id):
  """
  A view for editing user's product review
  """
  product = get_object_or_404(Product, slug=product_slug, pk=product_id)
  review = get_object_or_404(Review, pk=review_id)
  # make sure user is the review owner
  if request.user.id == review.buyer_id:
    if request.method == "POST":
      form = ReviewForm(request.POST, instance=review)
      if form.is_valid():
        form.save()
        messages.success(request, 'You have successfully updated your review')
        # redirect to the new product after save
        return redirect(Product.get_absolute_url(product))
    else:
      form = ReviewForm(instance=review)

    form_action = Review.get_edit_review_url(review)
    form_button = "Save Changes"

    context = { 'form': form, 'form_action': form_action, 'form_button': form_button }
    return render(request, 'review_form_edit.html', context)

  else:
    # if not product owner, raise 403 forbidden exception and render
    # 403.html template
    messages.error(request, 'You cannot edit this review')
    raise PermissionDenied

@login_required
def delete_review(request, product_slug, product_id, review_id):
  """
  A view that handles deleting user's existing product review
  """
  product = get_object_or_404(Product, slug=product_slug, pk=product_id)
  review = get_object_or_404(Review, pk=review_id)
  # make sure user is the review owner
  if request.user.id == review.buyer_id:
    review.delete()
    messages.success(request, 'You have successfully deleted your review')
    return redirect(Product.get_absolute_url(product))
  else:
    # if not product owner, raise 403 forbidden exception and render
    #  403.html template
    messages.error(request, 'You cannot delete this review')
    raise PermissionDenied