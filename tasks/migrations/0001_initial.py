# Generated by Django 3.2.6 on 2021-10-07 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('description', models.CharField(max_length=250, verbose_name='Описание')),
                ('deadline', models.DateField(verbose_name='Дата завершения')),
                ('attachment', models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d', verbose_name='Вложение')),
            ],
            options={
                'verbose_name': 'задачу',
                'verbose_name_plural': 'Задачи',
                'ordering': ['id'],
            },
        ),
    ]
