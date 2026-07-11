from django.test import TestCase
from django.urls import reverse

from .models import Task


class TaskCreateViewTests(TestCase):
    def test_create_task_view_saves_valid_form_and_redirects(self):
        response = self.client.post(
            reverse('task_create'),
            {
                'title': 'New task',
                'description': 'A newly created task',
                'status': 'pending',
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(Task.objects.filter(title='New task').exists())
        self.assertRedirects(response, reverse('task_list'))
