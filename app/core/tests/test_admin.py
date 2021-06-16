from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminSiteTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='test1@test.com',
            password='Test1234'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@test.com',
            password='Testpass123',
            name='Test User'
        )

    def test_users_listed(self):
        """Test that busers are listed on user page"""
        url = reverse('admin:core_user_changelist')
        respons = self.client.get(url)

        self.assertContains(respons, self.user.name)
        self.assertContains(respons, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add',)
        respons = self.client.get(url)

        self.assertEqual(respons.status_code, 200)
