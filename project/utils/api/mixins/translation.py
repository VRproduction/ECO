from rest_framework import serializers
from django.conf import settings

class TranslationMixin(serializers.ModelSerializer):
    @property
    def translation_suffixes(self):
        """Returns suffixes for each language defined in settings."""
        return [f"_{lang[0]}" for lang in settings.LANGUAGES]

    def get_translatable_fields(self):
        """
        Returns a list of fields that can be translated, including their translated versions.
        """
        base_fields = self.Meta.fields
        translatable_fields = []
        for field in base_fields:
            for suffix in self.translation_suffixes:
                translated_field_name = f"{field}{suffix}"
                translatable_fields.append(translated_field_name)
        return translatable_fields

    def to_representation(self, instance):
        """
        Returns the serialized representation of the instance with translations applied based on
        the Accept-Language header.
        """
        request = self.context.get('request')
        lang = request.headers.get('Accept-Language', settings.LANGUAGE_CODE)  # Default to settings.LANGUAGE_CODE

        supported_languages = [lang_code[0] for lang_code in settings.LANGUAGES]
        
        if lang not in supported_languages:
            lang = settings.LANGUAGE_CODE  # Fallback to default language
        
        data = super().to_representation(instance)
        
        if self.Meta.fields == '__all__':
            return self.get_all_fields(data, lang, supported_languages)
        else:
            return self.get_selected_fields(data, lang)

    def get_fields(self):
        fields = super().get_fields()  # Get base serializer fields first

        if self.Meta.fields == "__all__":
            # Add translated fields for all model fields if "__all__" is used.
            translatable_fields = self.get_translatable_fields()
        else:
            # Only add translated fields for explicitly listed fields.
            translatable_fields = [f"{field}{suffix}" 
                                  for field in self.Meta.fields
                                  for suffix in self.translation_suffixes]

        # Dynamically add translatable fields only if they exist on the model
        model_fields = self.Meta.model._meta.get_fields()  # Get model fields
        model_field_names = {field.name for field in model_fields}
        for field_name in translatable_fields:
            if field_name in model_field_names and field_name not in fields:
                fields[field_name] = serializers.CharField(required=False, allow_blank=True)

        return fields
    def get_all_fields(self, data, lang, supported_languages):
        """
        Applies translations to all fields and removes unnecessary ones.
        """
        fields = self.fields.keys()
        translated_fields = {}

        # Cache translatable fields
        for field_name in data:
            if field_name in fields:
                for lang_code in supported_languages:
                    if field_name.endswith(f"_{lang_code}"):
                        base_field = field_name[:-len(f"_{lang_code}")]
                        translated_fields.setdefault(base_field, []).append(field_name)

        # Apply translations and remove excess fields
        for base_field, translations in translated_fields.items():
            if f"{base_field}_{lang}" in translations:
                data[base_field] = data.pop(f"{base_field}_{lang}")
            else:
                # Keep original value if translation is missing
                data[base_field] = data.get(base_field, '')
            # Remove other translations
            for field_name in translations:
                if field_name != base_field:
                    data.pop(field_name, None)

        return data

    def get_selected_fields(self, data, lang):
        """
        Applies translations to only selected fields and removes other translatable fields.
        """
        translatable_fields = self.get_translatable_fields()
        new_data = {}

        for field in self.Meta.fields:
            translated_field_name = f"{field}_{lang}"
            if translated_field_name in data:
                new_data[field] = data.pop(translated_field_name)
            else:
                new_data[field] = data.pop(field, '')

        return new_data
