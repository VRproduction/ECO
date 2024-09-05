# serializers.py
from rest_framework import serializers

from apps.chat_bot.models import FAQ, FAQCategory

from utils.api.mixins.translation import TranslationMixin

class FAQSerializer(TranslationMixin):
    class Meta:
        model = FAQ
        fields = ['question', 'answer']

class FAQCategorySerializer(TranslationMixin):
    faqs = FAQSerializer(many=True)

    class Meta:
        model = FAQCategory
        fields = ['name', 'faqs']