from rest_framework import serializers

from .models import Org, OrgInvitation, OrgRelationship, OrgRole
from .utils import Role

class OrgSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # create the org
        instance = Org.objects.create(**validated_data)

        # create admin relationship object
        relationship = OrgRelationship.objects.get_or_create(
            org=instance, related_user=self.context['request'].user
        )[0]
        # assign the admin role
        role = OrgRole.objects.get_or_create(name=Role.ADMIN)[0]
        relationship.role = role
        relationship.save()

        # add this org to the users orgs
        self.context['request'].user.org_relationships.add(relationship)
        self.context['request'].user.save()

        return instance

    class Meta:
        model = Org
        fields = (
            "id",
            "name",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }

class OrgRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgRole
        fields = (
            "id",
            "name",
            "permissions",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "name": {"read_only": True},
            "permissions": {"read_only": True},
        }

class OrgRelationshipSerializer(serializers.ModelSerializer):
    role_permissions = serializers.SerializerMethodField(read_only=True)
    all_permissions = serializers.SerializerMethodField(read_only=True)

    def get_role_permissions(self, obj):
        return obj.get_role_permissions()

    def get_all_permissions(self, obj):
        return obj.get_all_permissions()

    class Meta:
        model = OrgRelationship
        fields = (
            "id",
            "org",
            "related_user",
            "role",
            "permissions",
            "role_permissions",
            "all_permissions",
            "permissions",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "org": {"read_only": True},
            "related_user": {"read_only": True},
            "role_permissions": {"read_only": True},
            "all_permissions": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


class OrgInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgInvitation
        fields = "__all__"
        extra_kwargs = {
            "id": {"read_only": True},
            "org": {"read_only": True},
            "invited_by": {"read_only": True},
            "accepted_at": {"read_only": True},
            "revoked_at": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }
