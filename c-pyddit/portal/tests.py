from django.test import TestCase


class ForumRedirectTests(TestCase):
    def test_forum_redirects_to_surveys(self):
        response = self.client.get('/g/forum/')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/surveys/')
