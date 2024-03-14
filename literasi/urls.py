from django.urls import path, include
from rest_framework import routers

from . import api
from . import views

app_name = 'literasi'

router = routers.DefaultRouter()
router.register("", api.LiterasiViewSet, basename="literasi")

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path('', views.LiterasiListView.as_view(), name="list") ,
]
