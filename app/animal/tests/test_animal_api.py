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
        'age': '5',
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

    def test_create_basic_animal(self):
        """Test creating a basic animal"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        payload = {
            'species': 'dog',
            'name': 'hanna',
            'breed': 'german',
            'age': '5',
            'gender': 'female',
            'support': 'ealfa',
            'visit_cost': 2,
            'med_cost': 2,
            'op_cost': 2,
            'food_cost': 2,
            'keep_cost': 2,
            'sum_cost': 10,
        }
        res = self.client.post(ANIMAL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        animal = Animal.objects.get(id=res.data['id'])
        for key in payload.keys():
            self.assertEqual(payload[key], getattr(animal, key))

    def test_create_animal_with_tags(self):
        """test creating animal with tags"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        tag1 = sample_tag(user=self.userad, name='wilds')
        tag2 = sample_tag(user=self.userad, name='urban')
        payload = {
            'species': 'dog',
            'name': 'hanna',
            'breed': 'german',
            'age': '5',
            'gender': 'female',
            'support': 'ealfa',
            'visit_cost': 2,
            'med_cost': 2,
            'op_cost': 2,
            'food_cost': 2,
            'keep_cost': 2,
            'sum_cost': 10,
            'tags': [tag1.id, tag2.id]
        }
        res = self.client.post(ANIMAL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        animal = Animal.objects.get(id=res.data['id'])
        tags = animal.tags.all()
        self.assertEqual(tags.count(), 2)
        self.assertIn(tag1, tags)
        self.assertIn(tag2, tags)

    def test_create_animal_with_workgroup(self):
        """test creating animal with workgroups"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)
        wg1 = sample_workgroup(user=self.userad, name='dogs')
        wg2 = sample_workgroup(user=self.userad, name='rescue')
        payload = {
            'species': 'dog',
            'name': 'hanna',
            'breed': 'german',
            'age': '5',
            'gender': 'female',
            'support': 'ealfa',
            'visit_cost': 2,
            'med_cost': 2,
            'op_cost': 2,
            'food_cost': 2,
            'keep_cost': 2,
            'sum_cost': 10,
            'work_group': [wg1.id, wg2.id]
        }
        res = self.client.post(ANIMAL_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        animal = Animal.objects.get(id=res.data['id'])
        wgs = animal.work_group.all()
        self.assertEqual(wgs.count(), 2)
        self.assertIn(wg1, wgs)
        self.assertIn(wg2, wgs)

    def test_partial_update_animal(self):
        """Test updating a animal with patch"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)

        animal = sample_animal(user=self.user)
        animal.tags.add(sample_tag(user=self.user))
        new_tag = sample_tag(user=self.user, name='healthy')

        payload = {'name': 'Helen', 'tags': [new_tag.id]}
        url = detail_url(animal.id)
        self.client.patch(url, payload)

        animal.refresh_from_db()
        self.assertEqual(animal.name, payload['name'])
        tags = animal.tags.all()
        self.assertEqual(len(tags), 1)
        self.assertIn(new_tag, tags)

    def test_full_update_animal(self):
        """Test updating a animal with put"""
        self.client = APIClient()
        self.client.force_authenticate(self.userad)

        animal = sample_animal(user=self.user)
        animal.tags.add(sample_tag(user=self.user))

        payload = {
            'species': 'dog',
            'name': 'jackie',
            'breed': 'german',
            'age': '5',
            'gender': 'male',
            'support': 'ealfa',
            'visit_cost': 5,
            'med_cost': 2,
            'op_cost': 2,
            'food_cost': 2,
            'keep_cost': 2,
            'sum_cost': 13,
        }
        url = detail_url(animal.id)
        self.client.put(url, payload)

        animal.refresh_from_db()
        self.assertEqual(animal.name, payload['name'])
        self.assertEqual(animal.visit_cost, payload['visit_cost'])
        self.assertEqual(animal.sum_cost, payload['sum_cost'])
        tags = animal.tags.all()
        self.assertEqual(len(tags), 0)
