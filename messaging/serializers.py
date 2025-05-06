from rest_framework import serializers

from .models import Message


class UpdateMessageSentBoolSerializer(serializers.Serializer):
    message_id = serializers.IntegerField()


class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = "__all__"
