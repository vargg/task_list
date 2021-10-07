from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import UserViewSet

router = DefaultRouter()

router.register('', UserViewSet)

urlpatterns = [
    path(
        'token/',
        TokenObtainPairView.as_view(),
        name='token',
    ),
    path('', include(router.urls)),
]
