from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe
from modeltranslation.admin import TranslationAdmin

from .models import (
    CompanyDepartment,
    Vacancy,
    VacancyType,
    WorkingHour,
    VacancyApplication
)
from .utils.filters import (
    ViewCountListFilter
)


@admin.action(description="Mark selected vacancies as published")
def make_published(self, request, queryset):
    queryset.update(status="PB")


@admin.action(description="Mark selected vacancies as draft")
def make_draft(self, request, queryset):
    queryset.update(status="DF")


@admin.register(CompanyDepartment)
class CompanyDepartmentAdmin(TranslationAdmin):
    readonly_fields = ('slug',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(VacancyType)
class VacancyTypeAdmin(TranslationAdmin):
    readonly_fields = ('slug',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(WorkingHour)
class WorkHourAdmin(TranslationAdmin):
    readonly_fields = ('slug',)

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }


@admin.register(Vacancy)
class VacancyAdmin(TranslationAdmin):

    class Media:
        js = (
            'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
            'modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
        }

    list_display = (
        'vacancy_title', 'salary', 'work_hour',
        'display_deadline_date', 'display_view_count', 
        'display_application_count',
        'status'
    )
    list_filter = (
        'created_at', 'department',
        'vacancy_type',
        'work_hour', 'status', 
        ViewCountListFilter
    )
    search_fields = (
        'vacancy_title', 'vacancy_content',
        'salary', 'vacancy_type__vacancy_type',
        'department__department_name',
        'department'
    )
    date_hierarchy = 'published_at'
    list_per_page = 20
    readonly_fields = ('slug', 'viewed_ips', 'application_count')
    actions = (make_published, make_draft)

    def display_deadline_date(self, obj):
        return obj.deadline_date
    display_deadline_date.short_description = 'Son müraciət tarixi'

    def display_view_count(self, obj):
        return obj.view_count
    display_view_count.short_description = 'Baxış sayı'

    def display_application_count(self, obj):
        return obj.application_count
    display_application_count.short_description = 'Müraciət sayı'


@admin.register(VacancyApplication)
class VacancyApplicationAdmin(admin.ModelAdmin):
    list_display = ( '__str__', 'display_vacancy', 'CV', 'display_apply_date')
    list_filter = ('created_at', 'vacancy')
    list_per_page = 20
    date_hierarchy = 'created_at'
    search_fields = (
        'vacancy__vacancy_title',
        'vacancy__vacancy_content' 
    )

    def display_vacancy(self, obj):
        url = reverse("admin:vacancies_vacancy_change", args=[obj.vacancy.id])
        link = '<a style="color: green;" href="%s">%s</a>' % (url, obj.vacancy)
        return mark_safe(link)
    display_vacancy.short_description = 'Vakansiya'

    def display_apply_date(self, obj):
        return obj.apply_date
    display_apply_date.short_description = 'Müraciət tarixi'
