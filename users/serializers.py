from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Profile, Satker

class SatkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Satker
        fields = '__all__'
        
class ProfileSerializer(serializers.ModelSerializer):
    detail_satker = SatkerSerializer(read_only=True, source='satker')
    satker = serializers.PrimaryKeyRelatedField(queryset=Satker.objects.all())
    # detail_satker = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = '__all__'
        
    # def get_detail_satker(self, obj):
    #     satker_obj = obj.satker
    #     return SatkerSerializer(satker_obj).data

        
class UserSerializer(serializers.ModelSerializer):
    last_login = serializers.SerializerMethodField()
    profile = ProfileSerializer(read_only=True)
    
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'is_staff', 'is_active', 'is_superuser', 'profile', 'last_login']
    
    def get_last_login(self, obj):
        return obj.last_login.strftime('%H:%M:%S - %d %B %Y') if obj.last_login else None