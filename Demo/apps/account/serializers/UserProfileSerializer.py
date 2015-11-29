from rest_framework import serializers
from apps.account.models import UserProfile
from apps.account.serializers.UserSerializer import UserSerializer


class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(instance=UserProfile.user, many=False)

    class Meta:
        model = UserProfile
        fields = ('profile_image', 'user',)