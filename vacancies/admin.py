from django.contrib import admin

from .models import Application, Company, Vacancy, Specialty


class ApplicationAdmin(admin.ModelAdmin):
    pass


class CompanyAdmin(admin.ModelAdmin):
    pass


class VacancyAdmin(admin.ModelAdmin):
    pass

class SpecialityAdmin(admin.ModelAdmin):
    pass

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Company, CompanyAdmin)
admin.site.register(Specialty, SpecialityAdmin)
admin.site.register(Vacancy, VacancyAdmin)
