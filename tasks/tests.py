from django.conf import settings
from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Task

User = get_user_model()


class TaskTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user_name',
            full_name='user_full_name',
            password='dfltusrpsswrd',
        )
        self.another_user = User.objects.create_user(
            username='another_user_name',
            full_name='another_user_full_name',
            password='dfltusrpsswrd',
        )
        self.client = APIClient()
        self.auth_client = APIClient()
        self.another_auth_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        another_refresh = RefreshToken.for_user(self.another_user)
        self.auth_client.credentials(
            HTTP_AUTHORIZATION=f'Token {refresh.access_token}'
        )
        self.another_auth_client.credentials(
            HTTP_AUTHORIZATION=f'Token {another_refresh.access_token}'
        )
        self.task = Task.objects.create(
            author=self.user,
            name='task_name',
            description='task_description',
            deadline='2021-10-10',
        )
        self.task.performers.add(self.user.id)

    def test_get_tasks_list(self):
        response = self.client.get('/tasks/')
        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе неавторизованного пользователя',
        )

        response = self.auth_client.get('/tasks/')
        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при доступе авторизованного пользователя',
        )

    def test_get_task(self):
        response = self.client.get('/tasks/1/')
        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе неавторизованного пользователя',
        )

        response = self.auth_client.get('/tasks/1/')
        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при доступе авторизованного пользователя',
        )

        response_data = response.json()
        self.assertEqual(
            response_data['name'],
            'task_name',
            'Ошибка в возвращаемых данных',
        )

    def test_create_task(self):
        data = {
            'name': 'new_task_name',
            'description': 'new_description',
            'deadline': '22.12.2222',
            'performers': [1]
        }
        cnt_before = Task.objects.count()
        response = self.client.post('/tasks/', data=data)
        cnt_after = Task.objects.count()

        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе неавторизованного пользователя',
        )
        self.assertEqual(
            cnt_before,
            cnt_after,
            'Внесение изменение в БД неавторизованным пользователем'
        )

        response = self.auth_client.post('/tasks/', data=data)
        cnt_after = Task.objects.count()
        response_data = response.json()

        self.assertEqual(
            response.status_code,
            201,
            'Неверный код ответа при доступе авторизованного пользователя',
        )
        self.assertEqual(
            cnt_before,
            cnt_after - 1,
            'Ошибка при добавлении записи в БД'
        )
        self.assertEqual(
            response_data['name'],
            data['name'],
            'Ошибка в возвращаемых данных'
        )

    def test_change_task(self):
        data = {
            'name': 'new_task_name'
        }
        response = self.client.patch('/tasks/1/', data=data)
        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе незарегистрированного '
            'пользователя',
        )
        self.assertEqual(
            Task.objects.get(id=1).name,
            'task_name',
            'Изменение данных в БД незарегистрированным пользователем',
        )

        response = self.another_auth_client.patch('/tasks/1/', data=data)
        self.assertEqual(
            response.status_code,
            403,
            'Неверный код ответа при доступе неавторизованного '
            'пользователя',
        )
        self.assertEqual(
            Task.objects.get(id=1).name,
            'task_name',
            'Изменение данных в БД неавторизованным пользователем',
        )

        response = self.auth_client.put('/tasks/1/', data=data)
        self.assertEqual(
            response.status_code,
            400,
            'Неверный код ответа при неправильном запросе',
        )
        self.assertEqual(
            Task.objects.get(id=1).name,
            'task_name',
            'Изменение данных в БД при неправильном запросе',
        )

        response = self.auth_client.patch('/tasks/1/', data=data)
        response_data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при изменении задачи',
        )
        self.assertEqual(
            response_data['name'],
            data['name'],
            'Ошибка в возвращаемых данных',
        )
        self.assertEqual(
            Task.objects.get(id=1).name,
            data['name'],
            'Ошибка при изменении данных в БД',
        )

        data['description'] = 'new_description'
        data['deadline'] = '11.11.2211'
        response = self.auth_client.put('/tasks/1/', data=data)
        response_data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при изменении задачи',
        )
        self.assertEqual(
            response_data['description'],
            data['description'],
            'Ошибка в возвращаемых данных',
        )
        self.assertEqual(
            Task.objects.get(id=1).description,
            data['description'],
            'Ошибка при изменении данных в БД',
        )

    def test_my_tasks(self):
        cnt_before = Task.objects.filter(author=self.user).count()
        response = self.auth_client.get('/tasks/my/')
        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при запросе задач пользователя'
        )
        self.assertEqual(
            cnt_before,
            len(response.json()['results']),
            'Ошибка в возвращаемых данных',
        )

        data = {
            'name': 'new_task_name',
            'description': 'new_task_description',
            'deadline': '11.11.2111'
        }

        self.auth_client.post('/tasks/', data=data)
        response = self.auth_client.get('/tasks/my/')
        self.assertEqual(
            cnt_before,
            len(response.json()['results']) - 1,
            'Ошибка в возвращаемых данных',
        )

    def test_del_task(self):
        cnt_before = Task.objects.filter(author=self.user).count()

        response = self.client.delete('/tasks/1/')
        cnt_after = Task.objects.filter(author=self.user).count()

        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе незарегистрированного '
            'пользователя',
        )
        self.assertEqual(
            cnt_before,
            cnt_after,
            'Внесение изменений незарегистрированным пользователем',
        )

        response = self.another_auth_client.delete('/tasks/1/')
        cnt_after = Task.objects.filter(author=self.user).count()

        self.assertEqual(
            response.status_code,
            403,
            'Неверный код ответа при доступе неавторизованного '
            'пользователя',
        )
        self.assertEqual(
            cnt_before,
            cnt_after,
            'Внесение изменений неавторизованным пользователем',
        )

        response = self.auth_client.delete('/tasks/1/')
        cnt_after = Task.objects.filter(author=self.user).count()

        self.assertEqual(
            response.status_code,
            204,
            'Неверный код ответа при доступе авторизованного '
            'пользователя',
        )
        self.assertEqual(
            cnt_before,
            cnt_after + 1,
            'Ошибка при внесении изменений в БД',
        )

    def test_tasks_pagination(self):
        new_tasks = 15
        pages, last_page_tasks = divmod(
            new_tasks + 1,
            settings.REST_FRAMEWORK['PAGE_SIZE']
        )
        pages += 1

        tasks = []

        for i in range(new_tasks):
            tasks.append(
                Task(
                    author=self.user,
                    name=f'n{i}',
                    description=f'd{i}',
                    deadline=f'21{i:02}-10-20'
                )
            )
        Task.objects.bulk_create(tasks)

        response = self.auth_client.get('/tasks/')
        response_data = response.json()

        self.assertEqual(
            response_data['count'],
            new_tasks + 1,
            'Ошибка в возвращаемых данных'
        )
        self.assertEqual(
            len(response_data['results']),
            settings.REST_FRAMEWORK['PAGE_SIZE'],
            'Ошибка в возвращаемых данных'
        )

        response = self.auth_client.get(f'/tasks/?page={pages}')
        response_data = response.json()

        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при доступе к странице'
        )
        self.assertEqual(
            len(response_data['results']),
            last_page_tasks,
            'Неверное количество задач на странице'
        )
