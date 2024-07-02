from typing import Any
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
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


class VacancyListView(ListView):
    context_object_name = 'vacancies'
    model = Vacancy
    paginate_by = 20 
    template_name = 'vacancies.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['vacancy_types'] = VacancyType.objects.all()
        context['job_types'] = JobType.objects.all()
        context['departments'] = CompanyDepartment.objects.all()
        context['working_hours'] = WorkingHour.objects.all()
        return context


class VacancyDetailView(DetailView):
    context_object_name = 'vacancy'
    model = Vacancy
    template_name = 'vacancy-detail.html'

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
