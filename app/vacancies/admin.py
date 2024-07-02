from django.contrib import admin

from .models import (
    CompanyDepartment,
    JobType,
    Vacancy,
    VacancyType,
    WorkingHour
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


admin.site.register(CompanyDepartment)
admin.site.register(JobType)
admin.site.register(VacancyType)
admin.site.register(WorkingHour)


@admin.register(Vacancy)
class VacancyAdmin(admin.ModelAdmin):
    list_display = (
        'vacancy_title', 'salary', 
        'job_type', 'work_hour',
        'deadline_date', 'view_count', 
        'status'
    )
    list_filter = (
        'created_at', 'department',
        'vacancy_type', 'job_type',
        'work_hour', 'status', 
        ViewCountListFilter
    )
    search_fields = (
        'vacancy_title', 'vacancy_content',
        'salary', 'vacancy_type__vacancy_type',
        'department__department_name',
        'department',
        'job_type__job_type'
    )
    date_hierarchy = 'published_at'
    list_per_page = 20
    readonly_fields = ('slug', 'viewed_ips')
    ordering = ('-updated_at', '-published_at')
    actions = (make_published, make_draft)



