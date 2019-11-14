import json

from django.test import Client
from django.urls import reverse
from django.test import TestCase


class ToDoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = '/todo_app/todos/'

    '''Success test cases start here'''

    def test_create_todo_and_create_bucket(self):
        req_body = {
            "name": "Need to complete payment integration",
            "done": False,
            "bucketName": "Tuesday",
        }
        response = self.client.post(reverse('Todos'),
                                    follow='True',
                                    data=json.dumps(req_body),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        req_body = {
            "name": "Need to complete payment integration",
            "done": False,
            "bucketId": 1,
            "bucketName": "Tuesday"
        }
        response = self.client.post(reverse('Todos'),
                                    follow='True',
                                    data=json.dumps(req_body),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_get_todolist(self):
        response = self.client.get(reverse('Todos'),
                                   follow='True',
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        req_body = {
            "name": "Need to complete payment integration",
            "done": False,
            "bucketId": 1,
            "bucketName": "Tuesday"
        }
        response = self.client.put(self.url+'40',
                                   follow='True',
                                   data=json.dumps(req_body),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_update_todo_and_create_bucket(self):
        req_body = {
            "name": "Need to complete payment integration",
            "done": True,
            "bucketName": "Tuesday"
        }
        response = self.client.put(self.url+'40',
                                   follow='True',
                                   data=json.dumps(req_body),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        response = self.client.delete(self.url+'40',
                                      follow='True',
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 200)
    '''Success test cases ends here'''


class BucketTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = '/todo_app/buckets'

    def test_get_bucket_list(self):
        response = self.client.get(reverse('Buckets'),
                                   follow='True',
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)
