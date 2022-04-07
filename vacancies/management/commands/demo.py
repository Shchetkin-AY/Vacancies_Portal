from django.core.management.base import BaseCommand

from vacancies.data import companies, jobs, specialties
from vacancies.models import Company, Specialty, Vacancy


class Command(BaseCommand):
    def handle(self, *args, **options):

        for company in companies:
            Company.objects.create(id=company["id"],
                                   name=company["title"],
                                   logo=company["logo"],
                                   employee_count=company["employee_count"],
                                   location=company["location"],
                                   description=company["description"])
        for specialty in specialties:
            Specialty.objects.create(**specialty)

        for job in jobs:
            Vacancy.objects.create(id=job['id'],
                                   title=job["title"],
                                   specialty=(Specialty.objects.get(code=job["specialty"])),
                                   company=Company.objects.get(id=job['company']),
                                   salary_min=job["salary_from"],
                                   salary_max=job["salary_to"],
                                   published_at=job["posted"],
                                   skills=job["skills"],
                                   description=job["description"])
