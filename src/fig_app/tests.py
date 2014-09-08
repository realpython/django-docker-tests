from django.test import TestCase


class SimpleTest(TestCase):

    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)


class HelloWorldTests(TestCase):

    def test_home_view_contains_hello_world(self):

        response = self.client.get('/')
        print response.content_type
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Hello")
