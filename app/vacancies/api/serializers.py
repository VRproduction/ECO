from django.utils import timezone
from django.core.exceptions import ValidationError

from rest_framework import serializers

from vacancies.models import VacancyApplication


class VacancyApplicationPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = VacancyApplication
        fields = (
            'id',
            'full_name',
            'email',
            'vacancy',
            'coverletter',
            'prtfolio_website',
            'CV'
        )

    def validate(self, attrs):
        attrs = super().validate(attrs)
        current_time = timezone.now()
        if attrs['vacancy'] and attrs['vacancy'].deadline:
            if attrs['vacancy'].deadline < current_time:
                raise ValidationError('Müraciətin vaxtı bitib')
        return attrs