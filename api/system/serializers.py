from rest_framework import serializers

from .models import Broadcast, WaitlistEntry

class BroadcastSerializer(serializers.ModelSerializer):
    class Meta:
        model = Broadcast
        fields = '__all__'

class WaitlistEntrySerializer(serializers.ModelSerializer):
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
            'time_until_can_accept': {'read_only': True},
        }