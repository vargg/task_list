from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from users.serializers import UserSerialiser

from .models import Task

User = get_user_model()


class PerformerSerialiser(UserSerialiser):
    id = serializers.IntegerField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'full_name',
        ]
        read_only_fields = [
            'username',
            'full_name',
        ]


class TaskSerializer(serializers.ModelSerializer):
    author = UserSerialiser(required=False)
    performers = PerformerSerialiser(many=True, required=False)

    class Meta:
        model = Task
        fields = '__all__'

    def to_internal_value(self, data):
        data = data.copy()
        try:
            performers_indexes = data.pop('performers')
        except KeyError:
            performers_indexes = None
        if performers_indexes is not None:
            data['performers'] = [
                {'id': i} for i in performers_indexes
            ]
        return super().to_internal_value(data)

    @transaction.atomic
    def create(self, validated_data):
        return self.executor(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        return self.executor(validated_data, task=instance)

    def executor(self, validated_data, task=None):
        try:
            performers = validated_data.pop('performers')
        except KeyError:
            performers = None
        if task is None:
            task = self.Meta.model.objects.create(**validated_data)
        else:
            old_performers = User.objects.filter(assigned_tasks=task)
            for user in old_performers:
                task.performers.remove(user)
            for key, value in validated_data.items():
                setattr(task, key, value)

        if performers is not None:
            for user in performers:
                task.performers.add(user['id'])
        task.save()
        return task
