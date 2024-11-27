from rest_framework import serializers
from .models import CustomUser, BloodTestRecord

from rest_framework import serializers, views
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'user_type']  # Include user_type here

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            user_type=validated_data['user_type']
        )
        return user

class RegisterView(views.APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BloodTestRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = BloodTestRecord
        fields = '__all__'
    
    def validate_value(self, value):
        if value < 0:
            raise serializers.ValidationError("Test value must be non-negative.")
        return value
