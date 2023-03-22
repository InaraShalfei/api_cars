from django.db import models


class Owner(models.Model):
    first_name = models.CharField(max_length=128)
    last_name = models.CharField(max_length=128)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Auto(models.Model):
    model = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    production_year = models.IntegerField(blank=True, null=True)
    engine_capacity = models.IntegerField(blank=True, null=True)
    owners = models.ManyToManyField(Owner, through='OwnerAuto')
    vin_code = models.IntegerField(unique=True)

    def __str__(self):
        return f'{self.model}'


class OwnerAuto(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE)
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
