from django.test import TestCase


class ShowTestCase(TestCase):
    """
    Test reading a crime report.
    """
    urls = 'crime.urls'
    fixtures = ['crime/fixtures/crimes']

    def setUp(self):
        pass

    def test_get_show_id(self):
        """
        Test accessing show id page which redirect to show title.
        """
        response = self.client.get('/show/1/')
        self.assertRedirects(response, '/title/terrible-crime/', status_code=301)

    def test_get_show_title(self):
        """
        Test accessing show page via slug.
        """
        response = self.client.get('/title/terrible-crime/')
        self.assertTemplateUsed(response, 'crime/show.html')

        self.assertEquals(response.context['crime'].id, 1)
        self.assertEquals(response.context['crime'].headline, "Terrible Crime")

    def tearDown(self):
        pass
