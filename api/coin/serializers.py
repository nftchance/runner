from rest_framework import serializers

from user.serializers import UserSerializer

from .models import Transfer

class TransferSerializer(serializers.ModelSerializer):
    from_user = UserSerializer(read_only=True)
    to_user = UserSerializer(read_only=True)

    class Meta:
        model = Transfer
        fields = '__all__'
        extra_kwargs = {
            'from_user': {'read_only': True},
            'to_user': {'read_only': True},
            'amount': {'read_only': True},
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
        }