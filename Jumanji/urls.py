"""Jumanji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


from vacancies.views import DetailVacancyView, MainView, VacanciesByCompanyView, \
    VacanciesListView, VacanciesBySpecialityView, SendVacancyView, MycompanyCreate, CompanyLetsstart, \
    CompanyVacancies, CompanyVacanciesCreate, CompanyEdit, CompanyVacanciesEdit

from accounts.views import LogoutFormView, RegisterUserView, LoginUserView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', MainView.as_view(), name="main"),
    path('vacancies/', VacanciesListView.as_view(), name="all_vacancies"),
    path('vacancies/cat/<str:code>', VacanciesBySpecialityView.as_view(), name="speciality"),
    path('companies/<int:id>', VacanciesByCompanyView.as_view(), name="company"),
    path('vacancies/<int:pk>', DetailVacancyView.as_view(), name="single_vakancy"),

    path('vacancies/<int:pk>/send', SendVacancyView.as_view(), name="send"),
    path('mycompany/letsstart', CompanyLetsstart.as_view(), name="company_edit"),
    path('mycompany/create', MycompanyCreate.as_view(), name="company_create"),
    path('mycompany', CompanyEdit.as_view(), name="my_company"),
    path('mycompany/vacancies', CompanyVacancies.as_view(), name="company_vacancies"),
    path('mycompany/vacancies/create', CompanyVacanciesCreate.as_view(), name="create_vacancy"),
    path('mycompany/vacancies/<int:vacancy_id>', CompanyVacanciesEdit.as_view(), name="update_vacancy"),

    path('login', LoginUserView.as_view(), name="login"),
    path('register', RegisterUserView.as_view(), name="register"),
    path('logout', LogoutFormView.as_view(), name="logout"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()

# handler404 = CustomHendler.custom_handler404
# handler500 = CustomHendler.custom_handler500
