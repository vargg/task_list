from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from .models import Task
from .permissions import AuthorOrReadOnly
from .serializers import TaskSerializer

User = get_user_model()


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [
        AuthorOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=False, methods=['GET', ])
    def my(self, request):
        queryset = self.queryset.filter(author=self.request.user)
        page = self.paginate_queryset(queryset)
        my_tasks = self.serializer_class(page, many=True)
        return self.get_paginated_response(my_tasks.data)
