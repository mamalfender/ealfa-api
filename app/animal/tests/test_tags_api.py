from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Tag
from animal.serializers import TagSerializer


TAGS_URL = reverse('animal:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """test the authorized user tags API"""

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

    def test_retrieve_tags(self):
        """test retrieving the tags"""
        Tag.objects.create(user=self.user, name='Wild')
        Tag.objects.create(user=self.user, name='Tame')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('id')
        serializer = TagSerializer(tags, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_tags_limited_to_user(self):
    #     """Test that tags returned are for authenticated user"""
    #     user2 = get_user_model().objects.create_user(
    #         'other@test.com',
    #         'testpass123'
    #     )
    #     Tag.objects.create(user=user2, name='Healthy')
    #     tag = Tag.objects.create(user=self.user, name='Sick')

    #     res = self.client.get(TAGS_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': 'Shiraz'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(
            user=self.userad,
            name=payload['name']
        ).exists()
        self.assertTrue(exists)

    def test_create_tag_invalid(self):
        """Test creating a new tag with invalid payload"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
