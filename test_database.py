from unittest import TestCase

from database import Client
from config import DB_PASSWORD


class Parent:
    client = Client(DB_PASSWORD, 'githubhelper', 'tokens')
    full_data = {'test_token': 'test_token', 'test_id': 'test_id'}
    data_with_id = {'test_id': 'test_id'}


class TestClient1(TestCase, Parent):
    def test_insert(self):
        result = self.client.insert(self.full_data)
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.inserted_id)


class TestClient2(TestCase, Parent):
    def test_get(self):
        result = self.client.get({'test_token': 'test_token'})
        self.assertIsNotNone(result)
        self.assertIsInstance(result, dict)
        self.assertEqual(result['test_id'], self.full_data['test_id'])

    def test_update(self):
        result = self.client.update({'test_token': 'test_token'}, {'test_token': 'test_token1'})
        self.assertTrue(result.acknowledged)
        self.assertIsNotNone(result.modified_count)
        updated_data = self.client.get(self.data_with_id)
        self.assertEqual(updated_data['test_token'], 'test_token1')


class TestClient3(TestCase, Parent):
    def test_delete(self):
        result = self.client.delete(self.data_with_id)
        self.assertIsNotNone(result)
        self.assertTrue(result.acknowledged)
        data = self.client.get(self.data_with_id)
        self.assertIsNone(data)
