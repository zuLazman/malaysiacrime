from django.test import TestCase



class MainTestCase(TestCase):
    """
    Test accessing and browsing crime reports.
    """
    fixtures = ['crimes', 'comments']

    def setUp(self):
        pass

    def test_get_index(self):
        """
        Test accessing index page.
        """
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'main/index.html')

        self.assertTrue(len(response.context['crimes']), 3)
        self.assertTrue(response.context['crimes'][0].id, 3)
        self.assertTrue(response.context['crimes'][0].id, 2)
        self.assertTrue(response.context['crimes'][0].id, 1)

    def tearDown(self):
        pass
