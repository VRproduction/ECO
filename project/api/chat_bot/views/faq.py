# views.py
from rest_framework import generics

from apps.chat_bot.models import FAQ, FAQCategory

from ..serializers.faq import FAQCategorySerializer

class FAQListView(generics.ListAPIView):
    queryset = FAQCategory.objects.prefetch_related('faqs').all()
    serializer_class = FAQCategorySerializer
