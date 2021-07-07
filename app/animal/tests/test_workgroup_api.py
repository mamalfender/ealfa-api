from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import WorkGroup
from animal.serializers import WorkGroupSerializer


WORKGROUP_URL = reverse('animal:workgroup-list')


class PublicWorkGroupApiTests(TestCase):
    """Test the publicly available WorkGroup API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving WorkGroup"""
        res = self.client.get(WORKGROUP_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkGroupApiTests(TestCase):
    """test the authorized user WorkGroup API"""

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

    def test_retrieve_workgroup(self):
        """test retrieving the WorkGroup"""
        WorkGroup.objects.create(user=self.user, name='DrVisit')
        WorkGroup.objects.create(user=self.user, name='Surgery')

        res = self.client.get(WORKGROUP_URL)

        workgroup = WorkGroup.objects.all().order_by('id')
        serializer = WorkGroupSerializer(workgroup, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_workgroup_limited_to_user(self):
    #     """Test that WorkGroup returned are for authenticated user"""
    #     user2 = get_user_model().objects.create_user(
    #         'other@test.com',
    #         'testpass123'
    #     )
    #     WorkGroup.objects.create(user=user2, name='Healthy')
    #     workgroup = WorkGroup.objects.create(user=self.user, name='Sick')

    #     res = self.client.get(WORKGROUP_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], workgroup.name)

    def test_create_workgroup_successful(self):
        """Test creating a new WorkGroup"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': 'Catch'}
        self.client.post(WORKGROUP_URL, payload)

        exists = WorkGroup.objects.filter(
            user=self.userad,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_workgroup_invalid(self):
        """Test creating a new WorkGroup with invalid payload"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': ''}
        res = self.client.post(WORKGROUP_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
