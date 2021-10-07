from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions as django_exceptions
from django.db import transaction
from rest_framework import serializers

User = get_user_model()


class UserSerialiser(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        fields = [
            'id',
            'username',
            'full_name',
            'password',
        ]
        model = User

    def validate(self, data):
        password = data.get('password')
        if password is not None:
            user_instance = User(**data)
            try:
                validate_password(password, user_instance)
            except django_exceptions.ValidationError as e:
                serializer_error = serializers.as_serializer_error(e)
                raise serializers.ValidationError(
                    {'password': serializer_error['non_field_errors']}
                )
        return data

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        try:
            password = validated_data.pop('password')
        except KeyError:
            password = None
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
