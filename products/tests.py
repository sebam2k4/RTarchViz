# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from .models import Product
from django.contrib.auth import get_user_model
from django.urls import reverse


class ProductModelTest(TestCase):
    """ Tests for Product Model """

    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        get_user_model().objects.create(
            id=1, username='test_user', email='test_user@gmail.com')
        Product.objects.create(id=1, name='1-name', price=10,
                               product_file='file_path',
                               seller=get_user_model().objects.get(id=1))

    def test_string_representation(self):
        product = Product(name="Product-1")
        self.assertEqual(str(product), product.name)

    def test_get_absolute_url(self):
        product = Product.objects.get(id=1)
        self.assertIsNotNone(product.get_absolute_url())

    def test_get_edit_product_url(self):
        product = Product.objects.get(id=1)
        self.assertIsNotNone(product.get_edit_product_url())

    def test_delete_product_url(self):
        product = Product.objects.get(id=1)
        self.assertIsNotNone(product.get_delete_product_url())

    def test_euro_price_method(self):
        product = Product.objects.get(id=1)
        euro_price = product.euro_price()
        self.assertEqual(euro_price, '€{0}'.format(product.price))


class PostListViewTest(TestCase):
    """ Tests for Product List view """

    @classmethod
    def setUpTestData(cls):
        """ Create 20 products for pagination tests """
        seller = get_user_model().objects.create(username='seller1',
                                                 email='seller1@gmail.com')
        number_of_products = 20
        for product_num in range(number_of_products):
            Product.objects.create(seller=seller, name='title {0}'.format(
                product_num), price=14, product_file='file_path')

    def setUp(self):
    self.user = get_user_model().objects.create(
        username='test_user', email='test_user@gmail.com')

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)

    # Test whether products show up on the Product list view:
    def test_one_product(self):
        Product.objects.create(name='1-name', price=10, seller=self.user)
        response = self.client.get('/products/')
        self.assertContains(response, '1-name')
        self.assertContains(response, 10)

    def test_two_products(self):
        Product.objects.create(name='1-name', price=10, seller=self.user)
        Product.objects.create(name='2-name', price=25, seller=self.user)
        response = self.client.get('/products/')
        self.assertContains(response, '1-name')
        self.assertContains(response, 10)
        self.assertContains(response, '2-name')
        self.assertContains(response, 25)

    # test pagination for Product list view:
    def test_pagination_is_9(self):
        response = self.client.get(reverse('products_list'))
        self.assertEqual(response.status_code, 200)
        # Confirm page has exactly 9 products
        self.assertEqual(len(response.context['products']), 9)

    def test_lists_all_posts(self):
        """ Get third page and confirm it has exactly 2 posts remaining """
        response = self.client.get(reverse('products_list')+'?page=3')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)

    def test_show_last_page_when_request_out_of_range(self):
        """ Get third page and confirm it has exactly 3 posts remaining """
        response = self.client.get(reverse('products_list')+'?page=50')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['products']), 2)


class ProductDetailViewTest(TestCase):
    """ Tests for Product Detail view """
    @classmethod
    def setUpTestData(cls):
        """ Set up non-modified objects used by all test methods """
        get_user_model().objects.create(
            id=1, username='test_user', email='test_user@gmail.com')
        Product.objects.create(id=1, name='1-name', price=10,
                               product_file='file_path',
                               seller=get_user_model().objects.get(id=1))

    def test_view_url_exists_at_desired_location(self):
        product = Product.objects.get(id=1)
        response = self.client.get(product.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def test_product_name(self):
        product = Product.objects.get(id=1)
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, product.name)

    def test_product_seller(self):
        product = Product.objects.get(id=1)
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, product.seller.username)

    def test_description_in_product(self):
        product = Product.objects.get(id=1)
        product.description = 'product description'
        product.save()
        response = self.client.get(product.get_absolute_url())
        self.assertContains(response, product.description)


class NewProductViewTest(TestCase):
    """ Tests for Add New Product View """

    def setUp(self):
        """ Create one user """
        test_user1 = get_user_model().objects._create_user(
            email='testuser1@gmail.com',
            username='testuser1',
            password='testtest1',
            is_staff=False,
            is_superuser=False
        )
        test_user1.save()

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('new_product'))
        self.assertRedirects(response, '/accounts/login/?next=/products/new/')

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email='testuser1@gmail.com',
                                  password='testtest1')
        response = self.client.get(reverse('new_product'))
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1@gmail.com')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'product_form_new.html')


class EditProductViewTest(TestCase):
    """ Tests for Edit Product View """

    def setUp(self):
        """ "Create one user """
        test_user1 = get_user_model().objects._create_user(
            email='testuser1@gmail.com',
            username='testuser1',
            password='testtest1',
            is_staff=False,
            is_superuser=False
        )
        test_user1.save()
        self.product = Product.objects.create(
            id=1, name='1-name', price=10, seller=test_user1)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.product.get_edit_product_url())
        self.assertRedirects(
            response, '/accounts/login/?next=/products/{0}--{1}/edit/'.format(
                self.product.slug, self.product.id))

    def test_logged_in_uses_correct_template(self):
        login = self.client.login(email='testuser1@gmail.com',
                                  password='testtest1')
        response = self.client.get(self.product.get_edit_product_url())
        # Check our user is logged in
        self.assertEqual(str(response.context['user']), 'testuser1@gmail.com')
        # Check that we got a response "success"
        self.assertEqual(response.status_code, 200)
        # Check we used correct template
        self.assertTemplateUsed(response, 'product_form_edit.html')


class DeleteProductViewTest(TestCase):
    """ Tests for delete Product View """

    def setUp(self):
        """ Create 1 user and 1 product"""
        test_user1 = get_user_model().objects._create_user(
            email='testuser1@gmail.com',
            username='testuser1',
            password='testtest1',
            is_staff=False,
            is_superuser=False
        )
        test_user1.save()
        self.product = Product.objects.create(
            id=1,
            name='1-name',
            price=10,
            seller=test_user1
        )

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(self.product.get_delete_product_url())
        self.assertRedirects(
            response, '/accounts/login/?next=/products/{0}--{1}/delete/'.format(
                self.product.slug, self.product.id))
