from django.contrib import admin
from django.db.models import Count


class ViewCountListFilter(admin.SimpleListFilter):
    title ="Baxış sayı"
    parameter_name = "view_count"

    def lookups(self, request, model_admin):

        return [
            ("less_than_50", "Baxış sayı: 0-50"),
            ("between_50_100", "Baxış sayı: 50-100"),
            ("between_100_200", "Baxış sayı: 100-200"),
            ("greater_than_200", "Baxış sayı: 200-dən çox")
        ]

    def queryset(self, request, queryset):
        queryset = queryset.annotate(views_count=Count('viewed_ips'))
        if self.value() == "less_than_50":
            return queryset.filter(views_count__lte=50)
    
        if self.value() == "between_50_100":
            return queryset.filter(
                views_count__gt=50,
                views_count__lte=100,
            )
        if self.value() == "between_100_200":
            return queryset.filter(
                views_count__gt=100,
                views_count__lte=200,
            )
        if self.value() == "greater_than_200":
            return queryset.filter(
                views_count__gt=200
            )

