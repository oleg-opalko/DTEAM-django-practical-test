from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from ..models import CV

class CVAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.cv_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'skills': 'Python, Django',
            'projects': 'Project 1, Project 2',
            'bio': 'Test bio',
            'contacts': 'test@example.com'
        }
        self.cv = CV.objects.create(**self.cv_data)
        self.url_list = reverse('cv-list')
        self.url_detail = reverse('cv-detail', args=[self.cv.id])

    def test_create_cv(self):
        """Test creating a new CV"""
        response = self.client.post(self.url_list, self.cv_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CV.objects.count(), 2)

    def test_retrieve_cv(self):
        """Test retrieving a CV"""
        response = self.client.get(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['first_name'], self.cv.first_name)

    def test_update_cv(self):
        """Test updating a CV"""
        updated_data = self.cv_data.copy()
        updated_data['first_name'] = 'Jane'
        response = self.client.put(self.url_detail, updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(CV.objects.get(id=self.cv.id).first_name, 'Jane')

    def test_delete_cv(self):
        """Test deleting a CV"""
        response = self.client.delete(self.url_detail)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CV.objects.count(), 0) 