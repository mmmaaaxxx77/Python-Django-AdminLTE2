from django.contrib.auth.models import User, Group, Permission
from rest_framework import serializers
from apps.account.serializers.GroupSerializer import GroupSerializer
from apps.account.serializers.PermissionSerializer import PermissionSerializer


class UserSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(instance=Group, many=True)
    user_permissions = PermissionSerializer(instance=Permission, many=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'last_login', 'date_joined', 'groups', 'user_permissions')