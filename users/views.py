from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet

from .permissions import CurrentUserOrAdminOrReadOnly
from .serializers import UserSerialiser

User = get_user_model()


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerialiser

    def get_permissions(self):
        if self.request.method == 'POST':
            return [AllowAny()]
        else:
            return [CurrentUserOrAdminOrReadOnly()]
