from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from store.models import Category, Item, InventoryChange
from django.contrib.auth import get_user_model

User = get_user_model()

class CategoryViewSetTest(TestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(email='testuser@mail.com', password='testpass', username='testuser')

        # Create some categories
        self.category1 = Category.objects.create(name='Electronics', creator=self.user)
        self.category2 = Category.objects.create(name='Clothing', creator=self.user)

        # API client
        self.client = APIClient()

    def test_list_categories(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make GET request to list categories
        response = self.client.get(reverse('category-list'))
        
        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of categories returned
        self.assertEqual(len(response.data), 2)

    def test_create_category(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Data to create a new category
        data = {"name": "Books"}

        # Make POST request to create a category
        response = self.client.post(reverse('category-list'), data)

        # Ensure the response is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the category was actually created
        self.assertEqual(Category.objects.count(), 3)
        self.assertEqual(Category.objects.get(name="Books").name, "Books")

    def test_update_category(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Data to update the existing category
        data = {"name": "Updated Electronics"}

        # Make PUT request to update the category
        response = self.client.put(reverse('category-detail', args=[self.category1.id]), data)

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the category was actually updated
        self.category1.refresh_from_db()
        self.assertEqual(self.category1.name, "Updated Electronics")

    def test_delete_category(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make DELETE request to delete a category
        response = self.client.delete(reverse('category-detail', args=[self.category1.id]))

        # Ensure the response is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the category was actually deleted
        self.assertEqual(Category.objects.count(), 1)


class ItemViewSetTest(TestCase):

    def setUp(self):
        # Create a user for authentication
        self.user = User.objects.create_user(email='testuser@mail.com', password='testpass', username='testuser')

        # Create a category and items
        self.category = Category.objects.create(name='Electronics', creator=self.user)
        self.item = Item.objects.create(name='Laptop', description='Gaming Laptop', quantity=5, price=1500, category=self.category, creator=self.user)

        # API client
        self.client = APIClient()

    def test_list_items(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make GET request to list items
        response = self.client.get(reverse('item-list'))

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check the number of items returned
        self.assertEqual(len(response.data), 4)

    def test_create_item(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Data to create a new item
        data = {
            "name": "Smartphone",
            "description": "Flagship smartphone",
            "quantity": 10,
            "price": 800,
            "category": self.category.id
        }

        # Make POST request to create an item
        response = self.client.post(reverse('item-list'), data)

        # Ensure the response is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Check that the item was actually created
        self.assertEqual(Item.objects.count(), 2)
        self.assertEqual(Item.objects.get(name="Smartphone").description, "Flagship smartphone")

    def test_update_item(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Data to update the existing item
        data = {"name": "Updated Laptop", "quantity": 3}

        # Make PUT request to update the item
        response = self.client.put(reverse('item-detail', args=[self.item.id]), data)

        # Ensure the response is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Check that the item was actually updated
        self.item.refresh_from_db()
        self.assertEqual(self.item.name, "Updated Laptop")
        self.assertEqual(self.item.quantity, 3)

    def test_delete_item(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make DELETE request to delete an item
        response = self.client.delete(reverse('item-detail', args=[self.item.id]))

        # Ensure the response is 204 No Content
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        # Check that the item was actually deleted
        self.assertEqual(Item.objects.count(), 0)
