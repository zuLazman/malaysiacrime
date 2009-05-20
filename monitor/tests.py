from django.core import mail
from django.test import TestCase

from models import Moniton


class MonitonTestCase(TestCase):
    """
    Test operations for crime areas monitoring.
    """
    urls = 'monitor.urls'

    def setUp(self):
        pass

    def test_get_subscribe(self):
        """
        Test accessing subscribe page.
        """
        response = self.client.get('/subscribe/')
        self.assertTemplateUsed(response, 'monitor/subscribe.html')

    def test_post_subscribe(self):
        """
        Test subscribing to monitor.
        """
        inputs = {
            'email': 'kegan@kegan.info',
            'north': 1.1234,
            'east': 1.1234,
            'south': 1.1234,
            'west': 1.1234,
        }

        response = self.client.post('/subscribe/', inputs)

        self.assertEquals(mail.outbox[0].to, [inputs['email']])
        self.assertEquals(mail.outbox[0].subject, 'Confirmation of Malaysia Crime Monitor subscription')
        self.assertRedirects(response, 'subscribe/done/?uuid=%s' % Moniton.objects.latest('created_at').add_uuid)

    def test_post_subscribe_email_invalid(self):
        """
        Test subscribing to monitor.
        """
        inputs = {
            'email': 'xxx',
            'north': 1.1234,
            'east': 1.1234,
            'south': 1.1234,
            'west': 1.1234,
        }

        response = self.client.post('/subscribe/', inputs, follow=True)
        self.assertFormError(response, 'form', 'email', 'Enter a valid e-mail address.')

    def tearDown(self):
        pass
