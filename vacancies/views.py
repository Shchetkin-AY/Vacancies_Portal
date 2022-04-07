from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count
from django.core.exceptions import ObjectDoesNotExist


from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect, reverse

from django.views.generic import ListView, TemplateView, View, CreateView, DetailView, UpdateView

from vacancies.forms import ApplicationForm, CompanyForm, VacancyForm
from vacancies.models import Company, Specialty, Vacancy, Application


class MainView(TemplateView):
    template_name = "public/index.html"

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context["speciality_list"] = Specialty.objects.annotate(vacancy_count=Count("vacancies"))
        context["company_list"] = Company.objects.annotate(vacancy_count=Count("vacancies"))
        return context


class VacanciesListView(ListView):
    model = Vacancy
    template_name = "public/vacancies.html"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(VacanciesListView, self).get_context_data(**kwargs)
        count_vacan = Vacancy.objects.aggregate(vacancy_count=Count("id"))
        context["count_vacancy"] = count_vacan["vacancy_count"]
        return context


class VacanciesBySpecialityView(ListView):
    template_name = "public/vacancies.html"

    def get_queryset(self):
        self.speciality = get_object_or_404(Specialty, code=self.kwargs["code"])
        self.queryset = self.speciality.vacancies.all()
        return super(VacanciesBySpecialityView, self).get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["speciality_title"] = self.speciality.title
        context["speciality_id"] = self.speciality.id
        spec_count = Specialty.objects.annotate(vacancy_count=Count("vacancies"))
        for count in spec_count:
            if self.speciality.id == count.id:
                context["count_vacancy"] = count.vacancy_count
        return context


class VacanciesByCompanyView(ListView):
    template_name = "public/company.html"

    def get_queryset(self):
        self.company = get_object_or_404(Company, pk=self.kwargs["id"])
        self.queryset = self.company.vacancies.all()
        return super(VacanciesByCompanyView, self).get_queryset()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context["company_name"] = self.company.name
        context["company_location"] = self.company.location
        context["company_id"] = self.company.id
        context["count_in_company"] = Company.objects.annotate(vacancy_count=Count("vacancies"))
        context["company_logo"] = self.company.logo
        return context


class DetailVacancyView(DetailView):
    model = Vacancy
    template_name = "vacancies/vacancy.html"
    form_class = ApplicationForm

    def get_context_data(self, form=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = form or self.form_class()
        return context

    def post(self, request, pk):
        form = self.form_class(request.POST)
        if form.is_valid():
            aplication = form.save(commit=False)
            aplication.user = request.user
            aplication.vacancy_id = pk
            aplication.save()
            return redirect("send", pk)
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data(form=form))


class SendVacancyView(View):
    template_name = "vacancies/send.html"

    def get(self, request, pk):
        return render(request, "vacancies/send.html")


class MycompanyCreate(LoginRequiredMixin, CreateView):
    template_name = 'company/company-edit.html'
    form_class = CompanyForm

    def get(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner_id=request.user.id)
            return redirect('company_edit')
        except ObjectDoesNotExist:
            return super().get(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyEdit(LoginRequiredMixin, UpdateView):
    template_name = 'company/company-edit.html'
    form_class = CompanyForm

    def get(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner_id=request.user.id)
        except ObjectDoesNotExist:
            return redirect('company_edit')
        return super().get(request, *args, **kwargs)

    def get_object(self, **kwargs):
        company = Company.objects.get(owner_id=self.request.user.id)
        return company

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class CompanyLetsstart(LoginRequiredMixin, TemplateView):
    template_name = 'company/company-create.html'



class CompanyVacancies(LoginRequiredMixin, ListView):
    model = Vacancy
    template_name = 'vacancies/vacancy-list.html'

    def get(self, request, *args, **kwargs):
        try:
            Company.objects.get(owner_id=request.user.id)
        except ObjectDoesNotExist:
            return redirect('company_edit')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = Vacancy.objects.filter(company__owner=self.request.user.id)
        return context


class CompanyVacanciesCreate(LoginRequiredMixin, CreateView):
    template_name = 'vacancies/vacancy-edit.html'
    form_class = VacancyForm

    def form_valid(self, form):
        form.instance.company = Company.objects.get(owner_id=self.request.user.id)
        return super().form_valid(form)


class CompanyVacanciesEdit(LoginRequiredMixin, UpdateView):
    template_name = 'vacancies/vacancy-edit.html'
    form_class = VacancyForm
    success_url = 'company_edit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['application'] = Application.objects.filter(
            vacancy__id=self.kwargs['vacancy_id']).annotate(count=Count('id'))
        return context

    def get_object(self, **kwargs):
        try:
            vacancy = Vacancy.objects.filter(company__owner=self.request.user).get(id=self.kwargs['vacancy_id'])
        except ObjectDoesNotExist:
            raise Http404
        return vacancy
