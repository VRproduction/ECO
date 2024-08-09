from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.product.models import Product, ProductCategory
from apps.config.models import APIKey



class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'category', 'price', 'stock')
        read_only_fields = ('slug',)

    def validate_category(self, value):
        """
        Validate that the category exists and return the category instance.
        """
        try:
            category = ProductCategory.objects.get(title=value)
        except ProductCategory.DoesNotExist:
            raise serializers.ValidationError(f"Category '{value}' does not exist.")
        return category

    def create(self, validated_data):
        category = validated_data.pop('category')
        api_key = self.context['request'].api_key

        product = Product.objects.create(
            category=category,
            created_by_supporter=api_key.supporter,
            is_active=False,
            is_test=api_key.is_test,
            **validated_data
        )

        if not api_key.is_test:
            self.send_email_to_admin(product, api_key.supporter)
        return product
    
    def send_email_to_admin(self, product: Product, supporter):
        site = Site.objects.get_current()
        site_url = site.domain
        
        title = f"Ecoproduct.az, {supporter} tərəfindən məhsul əlavə edildi"
        
        data = {
            'ttle': title,
            'product': product,
            'site_url': site_url,
        }

        message = render_to_string('mails/supporter_product_mail.html', data)

        send_mail(
            title, 
            message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False, html_message=message
        ) 
    
class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'slug')
        read_only_fields = ('slug',)
    