from rest_framework import serializers

from .models import Org, OrgInvitation


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )

class OrgInvitationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrgInvitation
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )