from modeltranslation.translator import (
    TranslationOptions, 
    register
)

from .models import (
    CompanyDepartment,
    JobType,
    VacancyType,
    WorkingHour,
    Vacancy
)

@register(CompanyDepartment)
class CompanyDepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name', )


@register(JobType)
class JobTypeTranslationOptions(TranslationOptions):
    fields = ('job_type', )


@register(VacancyType)
class VacancyTypeTranslationOptions(TranslationOptions):
    fields = ('vacancy_type', )


@register(WorkingHour)
class WorkingHourTranslationOptions(TranslationOptions):
    fields = ('work_hour', )


@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = ('vacancy_title', 'vacancy_content' )