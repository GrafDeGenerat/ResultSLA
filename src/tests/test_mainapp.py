import unittest

from src.mainapp.schemas import RequestModel as RQ
from src.mainapp.schemas import ResponseModel as RS
from src.mainapp.service import calculate_deadline
from src.tests.cases import cases_mainapp


class TestMainApp(unittest.TestCase):
    def setUp(self):
        self.mainapp = calculate_deadline

    def test_sla(self):
        for i, obj in enumerate(cases_mainapp, 1):
            data, expected = obj
            with self.subTest(i=i):
                self.assertEqual(self.mainapp(RQ(**data)), RS(**expected))


if __name__ == "__main__":
    unittest.main()
