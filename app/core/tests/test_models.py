from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def sample_user(email='test@test.com', password='testpass'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test whether creating a new user using email is successful"""
        email = 'test@test.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(email=email,
                                                    password=password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the user is normalized"""
        email = 'test@TEST.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invali_email(self):
        """Test creating user with no email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'Test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser"""
        user = get_user_model().objects.create_superuser(
            'test@test.com',
            'test123'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Neutered'
        )
        self.assertEqual(str(tag), tag.name)

    def test_workgroup_str(self):
        """Test the WorkGroup string representation"""
        workgroup = models.WorkGroup.objects.create(
            user=sample_user(),
            name='operation date'
        )
        self.assertEqual(str(workgroup), workgroup.name)

    def test_animal_str(self):
        """Test the animal string representation"""
        animal = models.Animal.objects.create(
            user=sample_user(),
            species='Dog',
            breed='German',
            name='max',
            age=2
            )
        concat = str(animal.species+' '+str(animal.name))
        self.assertEqual(str(animal), concat)
