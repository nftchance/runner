from rest_framework import serializers

from .models import Org


class OrgSerializer(serializers.ModelSerializer):
    class Meta:
        model = Org
        fields = "__all__"
        read_only_fields = (
            "id",
            "created_at",
            "updated_at",
        )
