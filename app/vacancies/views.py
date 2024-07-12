from typing import Any
from django.db.models.query import QuerySet
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.generic import (
    ListView,
    DetailView
)

from .models import (
    Vacancy,
    VacancyType,
    CompanyDepartment,
    JobType,
    WorkingHour,
    IPs)
from seo.models import VacancyPageSeo


class VacancyListView(ListView):
    context_object_name = 'vacancies'
    model = Vacancy
    queryset = Vacancy.published.order_by('-published_at')
    paginate_by = 10
    template_name = 'vacancy-list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy_types'] = VacancyType.objects.all()
        context['job_types'] = JobType.objects.all()
        context['departments'] = CompanyDepartment.objects.all()
        context['working_hours'] = WorkingHour.objects.all()
        context["seo"] = VacancyPageSeo.objects.first()
        context['vacancy_count'] = self.get_queryset().count
        return context
    
    def get_queryset(self):
        queryset = Vacancy.published.order_by('-published_at')
        department = self.request.GET.get('department')
        job_type = self.request.GET.get('jobtype')
        vacancy_type = self.request.GET.get('vactype')
        hour = self.request.GET.get('hour')
        salary = self.request.GET.get('salary')

        if department:
            queryset = queryset.filter(department__slug=department)

        if job_type:
            queryset = queryset.filter(job_type__slug=job_type)

        if vacancy_type:
            queryset = queryset.filter(vacancy_type__slug=vacancy_type)

        if hour:
            queryset = queryset.filter(work_hour__slug=hour)

        if salary:
            if salary != '2000':
                start, end = salary.split('-')
                queryset = queryset.filter(salary__gte=start, salary__lte=end)
            else:
                queryset = queryset.filter(salary__gte=salary)

        return queryset


class VacancyDetailView(DetailView):
    context_object_name = 'vacancy'
    model = Vacancy
    template_name = 'vacancy-single.html'

    def get(self, request: HttpRequest, slug, *args: Any, **kwargs: Any) -> HttpResponse:
        vacancy = get_object_or_404(Vacancy, slug=slug)
        ip = self.get_client_ip(request)
        ip_obj, created = IPs.objects.get_or_create(view_ip=ip)
        vacancy.viewed_ips.add(ip_obj)
        vacancy.save()
        return super().get(request, *args, **kwargs)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def get_context_data(self, **kwargs):
        cx = super().get_context_data(**kwargs)
        cx['vacancies'] = Vacancy.published.all()[:5]
        cx["seo"] = VacancyPageSeo.objects.first()
        cx['timezone_now'] = timezone.now() 
        return cx
