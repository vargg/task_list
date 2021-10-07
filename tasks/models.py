from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Task(models.Model):
    name = models.CharField(
        'Название',
        max_length=100,
    )
    description = models.CharField(
        'Описание',
        max_length=250,
    )
    deadline = models.DateField(
        'Дата завершения',
    )
    performers = models.ManyToManyField(
        User,
        verbose_name='Исполнители',
        blank=True,
        related_name='assigned_tasks',
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.PROTECT,
        related_name='created_tasks',
    )
    attachment = models.FileField(
        'Вложение',
        upload_to='files/%Y/%m/%d',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'задачу'
        verbose_name_plural = 'Задачи'
        ordering = ['id']

    def __str__(self):
        return f'Задача "{self.name}"'
