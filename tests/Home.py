from app import app
import unittest


class Success(unittest.TestCase):
    def setUp(self):
        set_app = app.test_client()
        self.response = set_app.get("/")

    def test_get(self):
        self.assertEqual(200, self.response.status_code)

    def test_content_type(self):
        self.assertIn("text/html", self.response.content_type)


if __name__ == "__main__":
    unittest.main()
