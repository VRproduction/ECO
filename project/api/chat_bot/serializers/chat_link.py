# serializers.py
from rest_framework import serializers

from apps.chat_bot.models import ChatLink


class ChatLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatLink
        fields = ['link',]

