import json

from django.test import Client
from django.urls import reverse
from django.test import TestCase


class ToDoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = Client()
        cls.url = '/todo/'

    '''Success test cases start here'''

    def test_create_todo_and_create_bucket(self):
        req_body = {
            "bucket__name": "Tuesday",
            "name": "Need to complete payment integration"
        }
        response = self.client.post(reverse('Todo'),
                                    follow='True',
                                    data=json.dumps(req_body),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_create_todo(self):
        req_body = {
            "name": "Need to complete payment integration",
            "bucket__id": 1,
            "bucket__name": "Tuesday"
        }
        response = self.client.post(reverse('Todo'),
                                    follow='True',
                                    data=json.dumps(req_body),
                                    content_type='application/json',
                                    )
        self.assertEqual(response.status_code, 200)

    def test_get_todolist(self):
        response = self.client.get(reverse('Todo'),
                                   follow='True',
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_update_todo(self):
        req_body = {
            "id": 1,
            "name": "Need to complete payment integration",
            "bucket__id": 1,
            "bucket__name": "Tuesday"
        }
        response = self.client.put(reverse('Todo'),
                                   follow='True',
                                   data=json.dumps(req_body),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_update_todo_and_create_bucket(self):
        req_body = {
            "id": 1,
            "name": "Need to complete payment integration",
            "bucket__name": "Tuesday"
        }
        response = self.client.put(reverse('Todo'),
                                   follow='True',
                                   data=json.dumps(req_body),
                                   content_type='application/json',
                                   )
        self.assertEqual(response.status_code, 200)

    def test_delete_todo(self):
        req_body = {
            "id": 1,
        }
        response = self.client.delete(reverse('Todo'),
                                      follow='True',
                                      data=json.dumps(req_body),
                                      content_type='application/json',
                                      )
        self.assertEqual(response.status_code, 200)
    '''Success test cases ends here'''
