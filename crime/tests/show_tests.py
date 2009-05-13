from django.test import TestCase


class ShowTestCase(TestCase):
    """
    Test reading a crime report.
    """
    urls = 'crime.urls'
    fixtures = ['crimes']

    def setUp(self):
        pass

    def test_get_show(self):
        """
        Test accessing show page.
        """
        response = self.client.get('/show/1/')
        self.assertTemplateUsed(response, 'crime/show.html')
        
        self.assertEquals(response.context['crime'].id, 1)
        self.assertEquals(response.context['crime'].headline, "Terrible Crime")

    def tearDown(self):
        pass
