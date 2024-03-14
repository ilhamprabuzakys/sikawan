from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from core.serializers import UserSerializer

from . import serializers

class UpdatePasswordView(APIView):
    def post(self, request):
        serializer = serializers.UpdatePasswordSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        current_password = serializer.validated_data.get('current_password')
        new_password = serializer.validated_data.get('new_password')
        
        if not user.check_password(current_password):
            return Response({'error': 'Password anda saat ini salah.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if new_password == current_password:
            return Response({'error': 'Password baru tidak boleh sama dengan password saat ini.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        
        # login(request, user)
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return Response({'message': 'Password anda berhasil diperbarui.'}, status=status.HTTP_200_OK)

class ResetPasswordView(APIView):
    def post(self, request):
        serializer = serializers.ResetPasswordSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        user_id = serializer.validated_data.get('user')
        
        user = User.objects.get(pk=user_id)
        
        new_password = '123456'
        nama_user = user.username
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': f'Password untuk user {nama_user} berhasil direset ke 123456'}, status=status.HTTP_200_OK)
    
        
class RequestResetPasswordView(APIView):
    def post(self, request):
        serializer = serializers.RequestResetPasswordSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data.get('email')
        
        user = User.objects.filter(email=email).first()
        
        if user:
            user_instance = UserSerializer(user).data
            return Response({
                'message': f'Akun dengan email {email} ditemukan',
                'user' : user_instance,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': f'Akun dengan email {email} tidak ditemukan',
            }, status=status.HTTP_404_NOT_FOUND)
    
        
