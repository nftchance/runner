import re

from rest_framework import serializers

from .models import Broadcast, WaitlistEntry


class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = '__all__'


class WaitlistEntrySerializer(serializers.ModelSerializer):
    def validate(self, data):
        if not 'id' in data:
            if 'email' in data and "+" in data['email']:
                data['email'] = re.sub(r"([+])\w+", "", data['email'])

        
            if WaitlistEntry.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError(
                    {"email": "Waitlist entry with email already exists."}
                )

        return data

    can_accept = serializers.SerializerMethodField()
    time_until_can_accept = serializers.SerializerMethodField()

    def get_can_accept(self, obj):
        return obj.can_accept()

    def get_time_until_can_accept(self, obj):
        return obj.time_until_can_accept()

    class Meta:
        model = WaitlistEntry
        fields = '__all__'
        extra_kwargs = {
            'can_accept': {'read_only': True},
            'user': {'read_only': True},
            'invited_at': {'read_only': True},
            'accepted_at': {'read_only': True},
            'time_until_can_accept': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }
