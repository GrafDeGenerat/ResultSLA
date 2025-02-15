import unittest

from src.mainapp.schemas import RequestModel, ResponseModel
from src.mainapp.service import calculate_deadline
from src.tests.cases import cases_mainapp


class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.mainapp = calculate_deadline

    def test_sla(self):
        for i, obj in enumerate(cases_mainapp, 1):
            data, expected = obj
            with self.subTest(i=i, name=data):
                self.assertEqual(
                    self.mainapp(RequestModel(**data)), ResponseModel(**expected)
                )


if __name__ == "__main__":
    unittest.main()
