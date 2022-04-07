from django import forms

from vacancies.models import User, Application, Company, Vacancy


class RegisterUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password",)


class LoginUserForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "password",)


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ("written_username", "written_phone", "written_cover_letter",)


class CompanyForm(forms.ModelForm):

    class Meta:
        model = Company
        fields = ("name", "location", "description", "employee_count")


class VacancyForm(forms.ModelForm):

    class Meta:
        model = Vacancy
        fields = ("title", "salary_min", "salary_max", "skills", "description", "specialty")
