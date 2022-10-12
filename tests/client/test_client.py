from unittest import TestCase

from atomic_red_team.client import Client


class ClientTestCases(TestCase):
    def test_get_test(self):
        client = Client()
        expected = next(client.iter_tests())
        result = client.get_test(test_id=expected['auto_generated_guid'])
        self.assertDictEqual(expected, result)

    def test_get_tests(self):
        client = Client()
        rows = client.iter_tests()
        for row in rows:
            self.assertIsInstance(row, dict)

    def test_count_tests(self):
        client = Client()
        expected = sum(1 for _ in client.iter_tests())
        result = client.count_tests()
        self.assertEqual(expected, result)

    def test_count_tests_by_technique_id(self):
        technique_ids = ['T1003']

        client = Client()
        expected = sum(1 for _ in client.iter_tests(technique_ids=technique_ids))
        result = client.count_tests(technique_ids=technique_ids)
        self.assertEqual(expected, result)
