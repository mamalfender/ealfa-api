from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import OpsDone
from dogs.serializers import OpsDoneSerializer


OPSDONE_URL = reverse('dogs:opsdone-list')


class PublicOpsDoneApiTests(TestCase):
    """Test the publicly available opsdone API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving opsdone"""
        res = self.client.get(OPSDONE_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOpsDoneApiTests(TestCase):
    """test the authorized user opsdone API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@testi.com',
            'passTest123'
        )
        self.userad = get_user_model().objects.create_user(
            'test@test.com',
            'passtest123',
            is_active=True,
            is_staff=True
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_opsdone(self):
        """test retrieving the opsdone"""
        OpsDone.objects.create(user=self.user, name='DrVisit')
        OpsDone.objects.create(user=self.user, name='Surgery')

        res = self.client.get(OPSDONE_URL)

        opsdone = OpsDone.objects.all().order_by('id')
        serializer = OpsDoneSerializer(opsdone, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_opsdone_limited_to_user(self):
    #     """Test that opsdone returned are for authenticated user"""
    #     user2 = get_user_model().objects.create_user(
    #         'other@test.com',
    #         'testpass123'
    #     )
    #     OpsDone.objects.create(user=user2, name='Healthy')
    #     opsdone = OpsDone.objects.create(user=self.user, name='Sick')

    #     res = self.client.get(OPSDONE_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], opsdone.name)

    def test_create_opsdone_successful(self):
        """Test creating a new opsdone"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': 'Catch'}
        self.client.post(OPSDONE_URL, payload)

        exists = OpsDone.objects.filter(
            user=self.userad,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_opsdone_invalid(self):
        """Test creating a new opsdone with invalid payload"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': ''}
        res = self.client.post(OPSDONE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
