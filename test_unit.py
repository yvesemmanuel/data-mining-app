from app import app
import unittest


class TestHome(unittest.TestCase):
    def setUp(self):
        set_app = app.test_client()
        self.response = set_app.get('/')

    def test_get(self):
        self.assertEqual(200, self.response.status_code)
