from rest_framework.test import APITestCase

from django.contrib.auth.models import User

class TestCutomerListCreateView(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user=User.objects.create_user(username='tsetuser',password='testpassword')

        cls.admin=User.objects.create_superuser(username='testadmin',password='testpassword')



    def test_customer_create_view(self):
        




