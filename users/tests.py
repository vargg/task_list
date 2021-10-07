from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class UserTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='user_name',
            full_name='user_full_name',
            password='dfltusrpsswrd',
        )
        self.client = APIClient()
        self.auth_client = APIClient()
        refresh = RefreshToken.for_user(self.user)
        self.auth_client.credentials(
            HTTP_AUTHORIZATION=f'Token {refresh.access_token}'
        )

    def test_get_users_info_list(self):
        response = self.client.get('/users/')
        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе неавторизованного пользователя',
        )

        response = self.auth_client.get('/users/')
        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при доступе авторизованного пользователя',
        )

    def test_get_user_info(self):
        response = self.client.get('/users/1/')
        self.assertEqual(
            response.status_code,
            401,
            'Неверный код ответа при доступе неавторизованного пользователя',
        )

        response = self.auth_client.get('/users/1/')
        self.assertEqual(
            response.status_code,
            200,
            'Неверный код ответа при доступе авторизованного пользователя',
        )

        data = response.json()
        self.assertEqual(
            data.get('id'),
            1,
            'Ошибка в возвращаемых данных',
        )
        self.assertEqual(
            data.get('username'),
            'user_name',
            'Ошибка в возвращаемых данных',
        )
        self.assertEqual(
            data.get('full_name'),
            'user_full_name',
            'Ошибка в возвращаемых данных',
        )

    def test_create_users(self):
        data = {
            'username': 'new_user_name',
        }
        response = self.client.post('/users/', data=data)

        self.assertEqual(
            response.status_code,
            400,
            'Неверный код ответа при неполных входных данных',
        )

        data['full_name'] = 'new_user_full_name'
        response = self.client.post('/users/', data=data)

        self.assertEqual(
            response.status_code,
            400,
            'Неверный код ответа при неполных входных данных',
        )

        data['password'] = 'dfltusrpsswrd'
        response = self.client.post('/users/', data=data)

        self.assertEqual(
            response.status_code,
            201,
            'Неверный код ответа при регистрации пользователя',
        )

        data = response.json()
        self.assertEqual(
            User.objects.count(),
            2,
            'Не соответствует количество пользователей после регистрации '
            'нового пользователя',
        )
        self.assertEqual(
            data.get('username'),
            data['username'],
            'Ошибка в возвращаемых данных при регистрации пользователя',
        )
        self.assertEqual(
            data.get('full_name'),
            data['full_name'],
            'Ошибка в возвращаемых данных при регистрации пользователя',
        )

    def test_change_user_info(self):
        data = {
            'username': 'changed_user_name_1'
        }

        response = self.auth_client.put('/users/1/', data=data)
        self.assertEqual(response.status_code, 400)

        response = self.auth_client.patch('/users/1/', data=data)
        self.assertEqual(response.status_code, 200)

        response_data = response.json()
        self.assertEqual(
            response_data.get('username'),
            data['username'],
            'Ошибка в возвращаемых данных после изменения данных пользователя',
        )
        self.assertEqual(
            User.objects.get(id=self.user.id).username,
            data['username'],
            'Ошибка в возвращаемых данных после изменения данных пользователя',
        )

        data = {
            'username': 'changed_user_name_2',
            'full_name': 'changed_full_name_2',
            'password': 'dfltusrpsswrd_2',
        }
        response = self.auth_client.put('/users/1/', data=data)
        self.assertEqual(response.status_code, 200)

    def test_del_user(self):
        data = {
            'username': 'new_user_name',
            'full_name': 'new_full_name',
            'password': 'dfltusrpsswrd',
        }
        response = self.client.post('/users/', data=data)
        response_data = response.json()
        client = APIClient()
        refresh = RefreshToken.for_user(
            User.objects.get(id=response_data['id'])
        )
        client.credentials(
            HTTP_AUTHORIZATION=f'Token {refresh.access_token}'
        )
        cnt_before = User.objects.count()
        response = self.client.delete(f'/users/{response_data["id"]}/')
        self.assertEqual(response.status_code, 401)

        response = self.auth_client.delete(f'/users/{response_data["id"]}/')
        self.assertEqual(response.status_code, 403)

        response = client.delete(f'/users/{response_data["id"]}/')
        cnt_after = User.objects.count()
        self.assertEqual(response.status_code, 204)
        self.assertEqual(cnt_before, cnt_after + 1)
