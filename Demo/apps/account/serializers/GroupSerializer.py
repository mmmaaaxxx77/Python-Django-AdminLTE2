from django.contrib.auth.models import User, Permission, Group
from rest_framework import serializers
from apps.account.serializers.PermissionSerializer import PermissionSerializer


class GroupSerializer(serializers.ModelSerializer):
    permissions = PermissionSerializer(instance=Permission, many=True)
    class Meta:
        model = Group
        fields = ('name', 'permissions')