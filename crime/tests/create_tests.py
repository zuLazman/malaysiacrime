from datetime import date
from django.test import TestCase

from crime.models import Crime


class CreateTestCase(TestCase):
    """
    Test creating crime report.
    """
    urls = 'crime.urls'

    def setUp(self):
        pass

    def test_get_create(self):
        """
        Test accessing create page.
        """
        response = self.client.get('/create/')
        self.assertTemplateUsed(response, 'crime/create.html')

    def test_post_create(self):
        """
        Test posting to create page.
        """
        inputs = {
            'headline': "Terrible Crime",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "G_DEFAULT_ICON",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "123456",
            'password2': "123456",
        }
        response = self.client.post('/create/', inputs)
        self.assertRedirects(response, '/title/terrible-crime/')

        crime = Crime.objects.latest('created_at')
        self.assertEquals(crime.headline, inputs['headline'])
        self.assertEquals(crime.date, inputs['date'])
        self.assertEquals(crime.location, inputs['location'])
        self.assertEquals(crime.icon, inputs['icon'])
        self.assertAlmostEquals(crime.lat, inputs['lat'])
        self.assertAlmostEquals(crime.lng, inputs['lng'])
        self.assertEquals(crime.details, inputs['details'])
        self.assertEquals(crime.author, inputs['author'])
        self.assertEquals(crime.password, inputs['password'])

    def test_post_create_password_not_match(self):
        """
        Test posting to create with password does not match.
        """
        inputs = {
            'headline': "Terrible Crime",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "G_DEFAULT_ICON",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "123456",
            'password2': "abcdef",
        }
        response = self.client.post('/create/', inputs)
        self.assertTemplateUsed(response, 'crime/create.html')
        self.assertFormError(response, 'form', 'password2', "The passwords do not match.")

    def test_post_create_icon_invalid(self):
        """
        Test creating with invalid icon string.
        """
        inputs = {
            'headline': "Terrible Crime",
            'date': date(2009,12,31),
            'location': "Ipoh, Perak",
            'icon': "XXX",
            'lat': 80,
            'lng': 60,
            'zoom': 18,
            'details': "Stealing of power.",
            'author': "Nizar",
            'password': "123456",
            'password2': "abcdef",
        }
        response = self.client.post('/create/', inputs)
        self.assertTemplateUsed(response, 'crime/create.html')
        self.assertFormError(response, 'form', 'icon', "Invalid icon.")

    def tearDown(self):
        pass
