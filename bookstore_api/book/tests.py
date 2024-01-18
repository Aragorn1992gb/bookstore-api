from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from django.contrib.auth.models import User, Group
from rest_framework.authtoken.models import Token
from .models import Book, Author, Editor


class BookViewTests(TestCase):
    def setUp(self):
        # Create a user without groups and obtain a token for authentication
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        # Create a stock_manager user and obtain a token for authentication
        self.sm_user = User.objects.create_user(username='testsmuser', password='testsmpassword')
        # Get or create the 'STOCK_MANAGER' group
        sm_group, created = Group.objects.get_or_create(name='STOCK_MANAGER')
        # Add the user to the 'STOCK_MANAGER' group
        self.sm_user.groups.add(sm_group)
        self.sm_token = Token.objects.create(user=self.sm_user)

        # Create an admin user and obtain a token for authentication
        self.admin_user = User.objects.create_user(username='testadminuser', password='testadminpassword')
        # Get or create the 'STOCK_MANAGER' group
        admin_user, created = Group.objects.get_or_create(name='ADMIN')
        # Add the user to the 'STOCK_MANAGER' group
        self.admin_user.groups.add(admin_user)
        self.admin_token = Token.objects.create(user=self.admin_user)
        
        self.author = Author.objects.create(name='J. R. R. Tolkien')
        self.editor = Editor.objects.create(name='Bompiani')
        self.book = Book.objects.create(id=1, title='The Lord Of The Rings', author=self.author, editor=self.editor, quantity=100, isbn="111111111111", barcode="111111111222")
        self.book.author = self.author
        self.book.editor = self.editor
        self.book.save()

        # Set up API client with authentication token for normal user
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        # Set up API client with authentication token for stock_manager user
        self.sm_client = APIClient()
        self.sm_client.credentials(HTTP_AUTHORIZATION=f'Token {self.sm_token.key}')

        # Set up API client with authentication token for admin user
        self.admin_client = APIClient()
        self.admin_client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')

    # Test GET book/book with a stock_manager
    def test_get_book_list_sm(self):
        # Generate the url
        url = reverse('book:book-list')
        response = self.sm_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'The Lord Of The Rings')

    # Test GET book/book with am user that doesn't are in any groups. Forbidden
    def test_get_book_list_nogroup_user(self):
        # Generate the url
        url = reverse('book:book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # Test GET book/book/{id} with a stock_manager
    def test_get_book_details_sm(self):
        # Generate the url
        url = reverse('book:book-detail', kwargs={'pk': self.book.id})
        response = self.sm_client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'The Lord Of The Rings')

    # Test POST book/remove-book by user admin. Forbidden
    def test_remove_book_admin(self):
        # Generate the url
        url = reverse('book:remove-book')
        data =  [{
            "id_book": 1,
            "quantity": 1,
            "single_price": 10,
            "reason": "Sold",
            "note": "string"
        }]

        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # Test POST book/remove-book by user stock_manager
    def test_remove_book_sm(self):
        # Generate the url
        url = reverse('book:remove-book')
        data =  [
                    {
                        "id_book": 1,
                        "quantity": 21,
                        "single_price": 10,
                        "reason": "Sold",
                        "note": "string"
                    }
                ]
        book_old=Book.objects.get(id=1)
        response = self.sm_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book_new=Book.objects.get(id=1)
        self.assertEqual(book_new.quantity, book_old.quantity - data[0]["quantity"])
        self.assertNotEqual(book_new.quantity, book_old.quantity + data[0]["quantity"])

    # Test POST book/remove-book by user stock_manager when book quantity if less then removing. Not Acceptable
    def test_remove_book_overflow_sm(self):
        # Generate the url
        url = reverse('book:remove-book')
        data =  [
                    {
                        "id_book": 1,
                        "quantity": 21,
                        "single_price": 1000,
                        "reason": "Sold",
                        "note": "string"
                    }
                ]
        response = self.sm_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    # Test POST book/remove-book by user stock_manager when book quantity=0. Not Acceptable
    def test_remove_book_quantity_zero_sm(self):
        # Generate the url
        url = reverse('book:remove-book')
        data =  [
                    {
                        "id_book": 1,
                        "quantity": 0,
                        "single_price": 1000,
                        "reason": "Sold",
                        "note": "string"
                    }
                ]
        response = self.sm_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    # Test POST book/remove-book by user stock_manager whith wrong body request. Not Acceptable
    def test_remove_book_overflow_sm(self):
        # Generate the url
        url = reverse('book:remove-book')
        data =  [
                    {
                        "book": 1,
                        "quantity": 21,
                        "single_price": 1000,
                        "reason": "Sold",
                        "note": "string"
                    }
                ]
        response = self.sm_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_406_NOT_ACCEPTABLE)

    # Test POST book/add-book by user stock_manager
    def test_add_book_sm(self):
        # Generate the url
        url = reverse('book:add-book')
        data =  [
                    {
                        "id_book": 1,
                        "quantity": 21,
                        "single_price": 1000,
                        "reason": "Sold",
                        "note": "string"
                    }
                ]
        book_old=Book.objects.get(id=1)
        response = self.sm_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        book_new=Book.objects.get(id=1)
        self.assertEqual(book_new.quantity, book_old.quantity + data[0]["quantity"])
        self.assertNotEqual(book_new.quantity, book_old.quantity - data[0]["quantity"])
        
    # Test POST book/manage_editor by user admin
    def test_manage_editor_admin(self):
        # Generate the url
        url = reverse('book:manage-editor-list')
        data =  {
                    "name": "TestName"
                }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    # Test POST book/manage_author by user stock_manager
    def test_manage_author_admin(self):
        # Generate the url
        url = reverse('book:manage-author-list')
        data =  {
                    "name": "TestName",
                    "surname": "TestSurname",
                    "birthdate": "2024-01-18"
                }
        response = self.admin_client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
