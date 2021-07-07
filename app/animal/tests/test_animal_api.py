from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Animal, Tag, WorkGroup
from animal.serializers import AnimalSerializer, AnimalDetailSerializer


ANIMAL_URL = reverse('animal:animal-list')


def detail_url(animal_id):
    """Return animal detail URL"""
    return reverse('animal:animal-detail', args=[animal_id])


def sample_tag(user, name='stray'):
    """create a sample tag"""
    return Tag.objects.create(user=user, name=name)


def sample_workgroup(user, name='Dogs'):
    """create a sample workgroup"""
    return WorkGroup.objects.create(user=user, name=name)


def sample_animal(user, **params):
    """create a sample animal"""
    defaults = {
        'species': 'dog',
        'name': 'jack',
        'breed': 'german',
        'age': 5,
        'gender': 'male',
        'support': 'ealfa',
        'visit_cost': 2,
        'med_cost': 2,
        'op_cost': 2,
        'food_cost': 2,
        'keep_cost': 2,
        'sum_cost': 10,
    }

    return Animal.objects.create(user=user, **defaults)


class PublicAnimalApiTests(TestCase):
    """Test the publicly available animal API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """test that login is required for retrieving animal"""
        res = self.client.get(ANIMAL_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateAnimalApiTests(TestCase):
    """test the authorized user animal API"""

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

    def test_retrieve_animal(self):
        """test retrieving the animal"""
        sample_animal(user=self.user)
        sample_animal(user=self.user)

        res = self.client.get(ANIMAL_URL)

        animal = Animal.objects.all().order_by('id')
        serializer = AnimalSerializer(animal, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    # def test_animal_limited_to_user(self):
    #     """Test that animal returned are for authenticated user"""
    #     user2 = get_user_model().objects.create_user(
    #         'other@test.com',
    #         'testpass123'
    #     )
    #     Animal.objects.create(user=user2, name='Healthy')
    #     animal = Animal.objects.create(user=self.user, name='Sick')

    #     res = self.client.get(ANIMAL_URL)

    #     self.assertEqual(res.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(res.data), 1)
    #     self.assertEqual(res.data[0]['name'], aninmal.name)

    def test_view_animal_detail(self):
        """test viewing an animal's detail"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        animal = sample_animal(user=self.userad)
        animal.tags.add(sample_tag(user=self.userad))
        animal.work_group.add(sample_workgroup(user=self.userad))

        url = detail_url(animal.id)
        res = self.client.get(url)

        serializer = AnimalDetailSerializer(animal)
        self.assertEqual(res.data, serializer.data)

    # def test_create_animal_successful(self):
    #     """Test creating a new animal"""
    #     self.client = APIClient()
    #     self.client.force_authenticate(self.userad)
    #     payload = {
    #         'species': 'dog',
    #         'name': 'hanna',
    #         'breed': 'german',
    #         'age': 5,
    #         'gender': 'female',
    #         'support': 'ealfa',
    #         'visit_cost': 2,
    #         'med_cost': 2,
    #         'op_cost': 2,
    #         'food_cost': 2,
    #         'keep_cost': 2,
    #         'sum_cost': 10,
    #     }
    #     self.client.post(ANIMAL_URL, payload)

    #     exists = Animal.objects.filter(
    #         user=self.userad,
    #         name=payload['name']
    #     ).exists()
    #     self.assertTrue(exists)

    # def test_create_animal_invalid(self):
    #     """Test creating a new animal with invalid payload"""
    #     self.client = APIClient()
    #     self.client.force_authenticate(self.userad)
    #     payload = {'name': ''}
    #     res = self.client.post(ANIMAL_URL, payload)

    #     self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
