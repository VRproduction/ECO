from modeltranslation.translator import (
    TranslationOptions, 
    register
)

from .models import (
    CompanyDepartment,
    VacancyType,
    WorkingHour,
    Vacancy
)

@register(CompanyDepartment)
class CompanyDepartmentTranslationOptions(TranslationOptions):
    fields = ('department_name', )


@register(VacancyType)
class VacancyTypeTranslationOptions(TranslationOptions):
    fields = ('vacancy_type', )


@register(WorkingHour)
class WorkingHourTranslationOptions(TranslationOptions):
    fields = ('work_hour', )


@register(Vacancy)
class VacancyTranslationOptions(TranslationOptions):
    fields = ('vacancy_title', 'vacancy_content' )