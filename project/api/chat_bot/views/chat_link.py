# views.py
from rest_framework import generics

from apps.chat_bot.models import ChatLink

from ..serializers.chat_link import ChatLinkSerializer

class ChatLinkView(generics.ListAPIView):
    queryset = ChatLink.objects.all()[:1]
    serializer_class = ChatLinkSerializer
