from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

router = routers.DefaultRouter()
router.register("users", api.UsersViewSet, basename="users")
router.register("profiles", api.ProfileViewSet, basename="profile")
router.register("satkers", api.SatkerViewSet, basename="satker")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('kelola_pengguna/', views.KelolaPenggunaView.as_view(), name="kelola_pengguna") ,
]
