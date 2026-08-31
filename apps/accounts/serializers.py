from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for creating a new user account.
    Validates input and securely hashes the password.
    """
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'},
        min_length=8
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'first_name', 'last_name')

    def create(self, validated_data):
        # We explicitly use create_user to ensure the password is hashed!
        # Do NOT use User.objects.create() here.
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            # They get the default CUSTOMER role as defined in models.py
        )
        return user


class UserProfileSerializer(serializers.ModelSerializer):
    """
    Serializer for returning public user information.
    Notice we DO NOT include the password field here.
    """
    role_display = serializers.CharField(source='get_role_display', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'role', 'role_display')
        read_only_fields = ('role', 'role_display') # Only admins should change roles!
