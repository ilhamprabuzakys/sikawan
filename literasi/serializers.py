from django.contrib.auth.models import User
from rest_framework import serializers

from . import models
from users.serializers import UserSerializer
        
class LiterasiSerializer(serializers.ModelSerializer):
    #created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = UserSerializer(many=False, read_only=True)
    
    class Meta:
        model = models.Literasi
        fields = '__all__'
        datatables_always_serialize = ['created_by', 'jumlah_diunduh']
    
    # def to_representation(self, instance):
    #     representation = super().to_representation(instance)
    #     created_by_data = instance.created_by
    #     user_serializer = UserSerializer(created_by_data)
    #     representation['created_by'] = user_serializer.data
    #     return representation