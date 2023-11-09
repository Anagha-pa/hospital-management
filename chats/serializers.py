from rest_framework import serializers
from .models import Message
from users.models import UserAccount as User


class MessageSerializer(serializers.ModelSerializer):
    message = serializers.CharField(source='content')
    user_id = serializers.IntegerField(source='sender_id')
    user_name = serializers.CharField(source = 'sender.name')
    class Meta:
        model = Message
        fields = ['message', 'user_id','user_name']

class ChatListSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    class Meta:
        fields = "__all__"

class ReceiverDetailsSerializer(serializers.Serializer):
    name = serializers.CharField()
    class Meta:
        fields = "__all__"

