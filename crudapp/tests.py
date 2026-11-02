
from django.test import TestCase
from django.urls import reverse
from .models import Product


class ProductCRUDTest(TestCase):

    def setUp(self):
        self.product = Product.objects.create(
            name="Laptop",
            description="Gaming laptop",
            price="1500.00"
        )

    # CREATE
    def test_product_create(self):
        response = self.client.post(
            reverse('product_create'),
            {
                'name': 'Phone',
                'description': 'New smartphone',
                'price': '800.00'
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Product.objects.filter(name='Phone').exists()
        )

    # READ
    def test_product_list(self):
        response = self.client.get(
            reverse('product_list')
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Laptop')

    # UPDATE
    def test_product_update(self):
        response = self.client.post(
            reverse('product_update', args=[self.product.pk]),
            {
                'name': 'Updated Laptop',
                'description': 'Updated description',
                'price': '2000.00'
            }
        )

        self.assertEqual(response.status_code, 302)

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, 'Updated Laptop')
        self.assertEqual(self.product.description, 'Updated description')
        self.assertEqual(str(self.product.price), '2000.00')

    # DELETE
    def test_product_delete(self):
        response = self.client.post(
            reverse('product_delete', args=[self.product.pk])
        )

        self.assertEqual(response.status_code, 302)

        self.assertFalse(
            Product.objects.filter(pk=self.product.pk).exists()
        )

    # TEST CREATE PAGE
    def test_product_create_page(self):
        response = self.client.get(
            reverse('product_create')
        )

        self.assertEqual(response.status_code, 200)

    # TEST UPDATE PAGE
    def test_product_update_page(self):
        response = self.client.get(
            reverse('product_update', args=[self.product.pk])
        )

        self.assertEqual(response.status_code, 200)

    # TEST DELETE PAGE
    def test_product_delete_page(self):
        response = self.client.get(
            reverse('product_delete', args=[self.product.pk])
        )

        self.assertEqual(response.status_code, 200)

    # TEST 404
    def test_product_not_found(self):
        response = self.client.get(
            reverse('product_update', args=[9999])
        )

        self.assertEqual(response.status_code, 404)
