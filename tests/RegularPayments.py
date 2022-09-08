from app import app
import unittest


class Success(unittest.TestCase):
    def setUp(self):
        set_app = app.test_client()
        self.response = set_app.post(
            "/analises/pagamentos_regulares", data={"municipio": "Afrânio"})

    def test_get(self):
        self.assertEqual(200, self.response.status_code)


class Fail(unittest.TestCase):
    def setUp(self):
        set_app = app.test_client()
        self.response = set_app.post(
            "/analises/pagamentos_regulares", data={"municipio": "Jamaica"})

    def test_get(self):
        self.assertEqual(500, self.response.status_code)


if __name__ == "__main__":
    unittest.main()
