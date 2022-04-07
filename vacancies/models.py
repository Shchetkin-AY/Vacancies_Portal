from django.db import models
from django.contrib.auth.models import User


class Specialty(models.Model):
    code = models.CharField(max_length=20)
    title = models.CharField(max_length=20)
    picture = models.ImageField(upload_to="MEDIA_SPECIALITY_IMAGE_DIR")


class Company(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=20)
    logo = models.ImageField(upload_to="MEDIA_COMPANY_IMAGE_DIR", null=True)
    description = models.TextField(max_length=100)
    employee_count = models.IntegerField()
    owner = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)


class Vacancy(models.Model):
    title = models.CharField(max_length=20)
    specialty = models.ForeignKey(Specialty, related_name="vacancies", on_delete=models.DO_NOTHING)
    company = models.ForeignKey(Company, related_name="vacancies", on_delete=models.DO_NOTHING)
    skills = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    salary_min = models.IntegerField()
    salary_max = models.IntegerField()
    published_at = models.DateField(auto_now_add=True)


class Application(models.Model):
    written_username = models.CharField(max_length=20)
    written_phone = models.IntegerField()
    written_cover_letter = models.TextField(max_length=200)
    vacancy = models.ForeignKey(Vacancy, related_name="applications", on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name="applications", on_delete=models.CASCADE)
