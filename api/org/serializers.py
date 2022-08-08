from rest_framework import serializers

from .models import Org, OrgInvitation, OrgRelationship, OrgRole


class OrgSerializer(serializers.ModelSerializer):
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


class OrgRelationshipSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgRelationship
        fields = (
            "id",
            "org",
            "related_user",
            "role",
            "permissions",
            "created_at",
            "updated_at",
        )
        extra_kwargs = {
            "id": {"read_only": True},
            "org": {"read_only": True},
            "related_user": {"read_only": True},
            "created_at": {"read_only": True},
            "updated_at": {"read_only": True},
        }


# TODO: see what can be done about using a nested serializer for invited_user
class OrgInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgInvitation
        fields = "__all__"
        read_only_fields = (
            "id",
            "org",
            "invited_by",
            "accepted_at",
            "revoked_at",
            "created_at",
            "updated_at",
        )
