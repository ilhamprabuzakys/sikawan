from rest_framework import serializers

class UpdatePasswordSerializer(serializers.Serializer):
    current_password = serializers.CharField(max_length=128, write_only=True)
    new_password = serializers.CharField(max_length=128, write_only=True)

class ResetPasswordSerializer(serializers.Serializer):
    user = serializers.IntegerField(write_only=True)

class RequestResetPasswordSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=128, write_only=True)