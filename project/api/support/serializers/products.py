from django.conf import settings
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.models import Site

from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from apps.product.models import Product, ProductCategory
from apps.config.models import APIKey



class ProductCategorySerializer(ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id', 'title', 'slug')
        read_only_fields = ('slug',)
    
    def create(self, validated_data):
        api_key = self.context['request'].api_key

        product_category = ProductCategory.objects.create(
            created_by_supporter=api_key.supporter,
            is_active=False,
            is_test=api_key.is_test,
            **validated_data
        )

        if not api_key.is_test:
            self.send_email_to_admin(product_category, api_key.supporter)
        return product_category
    
    def send_email_to_admin(self, product_category: ProductCategory, supporter):
        site = Site.objects.get_current()
        site_url = site.domain
        
        title = f"Ecoproduct.az, {supporter} tərəfindən kateqoriya əlavə edildi"
        
        data = {
            'title': title,
            'product_category': product_category,
            'site_url': site_url,
        }

        message = render_to_string('mails/supporter_product_category_mail.html', data)

        send_mail(
            title, 
            message,
            settings.EMAIL_HOST_USER,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False, html_message=message
        ) 

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.CharField()
    # product_id = serializers.CharField(source='logix_product_id')  # logix_product_id'yi product_id olarak adlandır

    class Meta:
        model = Product
        fields = ('id', 'title', 'slug', 'category', 'price', 'stock', 'logix_product_id')
        read_only_fields = ('slug',)

    def validate_category(self, value):
        """
        Validate if the category exists. If not, create a new one using ProductCategorySerializer with additional fields.
        """
        category = ProductCategory.objects.filter(title=value).first()
        if not category:
            api_key = self.context['request'].api_key
            category_data = {
                'title': value, 
                'is_active': False,
                'is_test': api_key.is_test,
                'created_by_supporter': api_key.supporter,
            }

            category_serializer = ProductCategorySerializer(data=category_data, context=self.context)
            if category_serializer.is_valid():
                category = category_serializer.save()
            else:
                raise serializers.ValidationError(category_serializer.errors)
        
        return category


    def create(self, validated_data):
        category = validated_data.pop('category')
        api_key = self.context['request'].api_key

        # Check if a product with the same title already exists
        existing_product = Product.objects.filter(logix_product_id=validated_data.get('logix_product_id')).first()

        if existing_product:
            # If product exists, update price, stock, and category
            existing_product.price = validated_data.get('price', existing_product.price)
            existing_product.stock = validated_data.get('stock', existing_product.stock)
            existing_product.title = validated_data.get('title', existing_product.title)
            existing_product.is_test = api_key.is_test
            existing_product.category = category  # Update the category as well
            existing_product.save()
            return existing_product

        # Create new product if not exists
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
            'title': title,
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