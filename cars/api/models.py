from django.db import models

from .choices import CHOICES


class Owner(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)
    date_of_birth = models.IntegerField(default=1990)
    nationality = models.CharField(max_length=25, choices=CHOICES, default='Казахстан')

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Auto(models.Model):
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    production_year = models.IntegerField(blank=True, null=True)
    engine_capacity = models.IntegerField(blank=True, null=True)
    owners = models.ManyToManyField(Owner, through='OwnerAuto', related_name='autos')
    vin_code = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.model}'


class OwnerAuto(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
