from datetime import datetime

from django.core import mail
from django.core.management import call_command
from django.test import TestCase

from models import Log, Moniton


class MonitonTestCase(TestCase):
    """
    Test operations for crime areas monitoring.
    """
    urls = 'monitor.urls'
    fixtures = ['monitor/fixtures/monitons.json', 'monitor/fixtures/crimes.json', 'monitor/fixtures/logs.json']

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
            'zoom': 9,
        }
        response = self.client.post('/subscribe/', inputs)

        self.assertEquals(mail.outbox[0].to, [inputs['email']])
        self.assertEquals(mail.outbox[0].subject, 'Confirmation of Malaysia Crime Monitor subscription')
        self.assertRedirects(response, 'subscribe/done/%s/' % Moniton.objects.latest('created_at').add_uuid)

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
            'zoom': 9,
        }
        response = self.client.post('/subscribe/', inputs, follow=True)
        self.assertFormError(response, 'form', 'email', 'Enter a valid e-mail address.')

    def test_get_subscribe_confirm(self):
        """
        Test confirmation a subscription.
        """
        response = self.client.get('/subscribe/confirm/%s/' % '03619ac2453211de8c651fabc0151a16')
        self.assertTemplateUsed(response, 'monitor/subscribe_confirm.html')

        self.assertEquals(response.context['moniton'].email, 'unconfirm@example.com')
        self.assertTrue(Moniton.objects.get(email='unconfirm@example.com').registered)

    def test_get_subscribe_confirm_uuid_invalid(self):
        """
        Test confirmation a subscription.
        """
        response = self.client.get('/subscribe/confirm/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def test_get_unsubscribe_done(self):
        """
        Test requesting email for unsubscription confirmation.
        """
        response = self.client.get('/unsubscribe/done/%s/' % '45368b7c454311de829b33b9aa2110db')
        self.assertTemplateUsed(response, 'monitor/unsubscribe_done.html')

        self.assertEquals(mail.outbox[0].to, ['confirm1@example.com'])
        self.assertEquals(mail.outbox[0].subject, 'Confirmation of Malaysia Crime Monitor unsubscription')

    def test_get_unsubscribe_done_uuid_invalid(self):
        """
        Test requesting email for unsubscription confirmation with invalid uuid.
        """
        response = self.client.get('/unsubscribe/done/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def test_get_unsubscribe_confirm(self):
        """
        Test confirmation an unsubscription.
        """
        response = self.client.get('/unsubscribe/confirm/%s/' % '4ad2302c454311de8b3387c74347e6f7')
        self.assertTemplateUsed(response, 'monitor/unsubscribe_confirm.html')
        self.assertFalse(Moniton.objects.filter(email='confirm@example.com'))

    def test_get_unsubscribe_confirm_uuid_invalid(self):
        """
        Test confirmation an unsubscription with invalid uuid.
        """
        response = self.client.get('/unsubscribe/confirm/', {'uuid': 'xxx'})
        self.assertTemplateUsed(response, '404.html')

    def test_get_area(self):
        """
        Test showing the area of subscription.
        """
        response = self.client.get('/area/%s/' % '45368b7c454311de829b33b9aa2110db')
        self.assertTemplateUsed(response, 'monitor/area.html')
        self.assertEquals(response.context['moniton'], Moniton.objects.get(pk=2))

    def test_monitor_initial_log_creation(self):
        """
        Test creating of first log, when not log data is available.
        """
        Log.objects.all().delete()
        call_command("send_all", '1238860800') # Timestamp for 2009-04-05.
        log = Log.objects.all().latest('created_at')

        self.assertEquals(log.start, log.end)

    def test_monitor_subsequest_log_creation(self):
        """
        Test creating of subsequent log entry.
        """
        call_command("send_all", '1238860800') # Timestamp for 2009-04-05.
        log = Log.objects.all().latest('created_at')

        self.assertEquals(log.start, datetime(2009, 04, 05, 0, 0))
        self.assertTrue(log.start < log.end)

    def test_monitor_notification(self):
        """
        Test the correctness of notifications.
        """
        call_command("send_all", '1238860800') # Timestamp for 2009-04-05.

        self.assertEquals(len(mail.outbox), 2)

        self.assertEquals(mail.outbox[0].to, ['confirm1@example.com'])
        self.assertNotEquals(mail.outbox[0].body.rfind('Terrible Crime Middle In Date'), -1)
        self.assertNotEquals(mail.outbox[0].body.rfind('Terrible Crime East'), -1)

        self.assertEquals(mail.outbox[1].to, ['confirm2@example.com'])
        self.assertNotEquals(mail.outbox[1].body.rfind('Terrible Crime Middle In Date'), -1)
        self.assertNotEquals(mail.outbox[1].body.rfind('Terrible Crime West'), -1)

    def tearDown(self):
        pass


# Disabled TEMPLATE_DIRS so that custom templates would not intefere with tests.
from django.conf import settings
settings.TEMPLATE_DIRS = ()
