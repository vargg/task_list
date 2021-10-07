from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    full_name = models.CharField(
        verbose_name='Полное имя',
        max_length=250,
    )
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = [
        'full_name',
    ]

    class Meta:
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']

    def __repr__(self):
        return (
            f'{self.__cls__.__name__}(full_name={self.full_name}, '
            f'username={self.username})'
        )

    def __str__(self):
        return f'Пользователь {self.full_name} ({self.username}).'
