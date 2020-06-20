from django.urls import path, include

from api import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r"", views.UserSignUpViewSet)

urlpatterns = [
    path("", include(router.urls)),
]