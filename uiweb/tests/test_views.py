from django.http import response
from django.test import TestCase,Client
from django.urls import reverse, resolve
from apidatabase.models import Store, Advertisement
import json
class TestViews(TestCase):
    def setUp(self):
        self.client=Client()
        self.home_url = reverse('Home_Page')



    def test_home(self):
        client=Client() #setUp
        response=client.get(self.home_url)

        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,"uiweb/home3.html")

    def test_login(self):
        pass    