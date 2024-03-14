from django.core.mail import send_mail
from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from django.contrib.auth.models import User

from core.serializers import UserSerializer
from core import pagination

from . import serializers
from . import models
from . import filters
from . import signals

class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.annotate(profile_updated_at=F('profile__updated_at')).order_by('-profile_updated_at')
    serializer_class = serializers.UserSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = filters.UserFilter
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = pagination.Page10NumberPagination
    
    # Membuat data profile ketika dibuatnya user
    def perform_create(self, serializer):
        satker_id = self.request.data.get('satker')
        notelp = self.request.data.get('notelp')
        direktorat = 'dayatif'
        
        user_instance = serializer.save()
        
        signals.create_profile_for_user(sender=self.__class__, instance=user_instance, created=True, satker_id=satker_id, notelp=notelp, direktorat=direktorat)
    
    # Memperbarui data profile ketika diperbaruinya data user
    def perform_update(self, serializer):
        data = { "satker": self.request.data.get('satker'), "notelp": self.request.data.get('notelp') }
        
        profile_instance = serializer.instance.profile
        profile_serializer = serializers.ProfileSerializer(profile_instance, data=data, partial=True)
        
        if not profile_serializer.is_valid():
            serializer.save()
        else:
            profile_serializer.save()
            serializer.save()

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = models.Profile.objects.all()
    serializer_class = serializers.ProfileSerializer
    permission_classes = [permissions.IsAuthenticated,]
    pagination_class = pagination.Page10NumberPagination
    
    # Memperbarui data profile ketika diperbaruinya data user
    def perform_update(self, serializer):
        data = {
            "first_name": self.request.data.get('first_name'),
            "last_name": self.request.data.get('last_name'),
            "email": self.request.data.get('email'),
        }
        
        user_instance = serializer.instance.user
        user_serializer = serializers.UserSerializer(user_instance, data=data, partial=True)
        
        if not user_serializer.is_valid():
            serializer.save()
        else:
            user_serializer.save()
            serializer.save()
    
class SatkerViewSet(viewsets.ModelViewSet):
    queryset = models.Satker.objects.all()
    serializer_class = serializers.SatkerSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = filters.SatkerFilter
    pagination_class = pagination.Page10NumberPagination
