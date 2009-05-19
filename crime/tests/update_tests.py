from datetime import date
from django.test import TestCase

from crime.models import Crime


class UpdateTestCase(TestCase):
    """
    Test updating a crime report.
    """
    urls = 'crime.urls'
    fixtures = ['crime/fixtures/crimes']

    def setUp(self):
        pass

    def test_get_update(self):
        """
        Test accessing update page.
        """
        response = self.client.get('/update/1/')
        self.assertTemplateUsed(response, 'crime/update.html')

        self.assertEquals(response.context['crime'].id, 1)
        self.assertEquals(response.context['crime'].headline, "Terrible Crime")

    def test_post_update(self):
        """
        Test post update page.
        """
        inputs = {
            'headline': "Terrible Crime Updated",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "G_DEFAULT_ICON",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "123456",
        }
        response = self.client.post('/update/1/', inputs)
        self.assertRedirects(response, '/show/1/')

        crime = Crime.objects.get(pk=1)
        self.assertEquals(crime.headline, inputs['headline'])

    def test_post_update_password_unmatch(self):
        """
        Test post update with unmatch password.
        """
        inputs = {
            'headline': "Terrible Crime Updated",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "G_DEFAULT_ICON",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "aaaaaa",
        }
        response = self.client.post('/update/1/', inputs)
        self.assertTemplateUsed(response, 'crime/update.html')
        self.assertFormError(response, 'form', 'password', "The password is incorrect.")

    def test_post_update_icon_invalid(self):
        """
        Test post update with invalid icon.
        """
        inputs = {
            'headline': "Terrible Crime Updated",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "XXX",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "aaaaaa",
        }
        response = self.client.post('/update/1/', inputs)
        self.assertTemplateUsed(response, 'crime/update.html')
        self.assertFormError(response, 'form', 'icon', "Invalid icon.")

    def tearDown(self):
        pass
