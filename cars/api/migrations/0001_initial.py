# Generated by Django 3.2.5 on 2023-03-22 14:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Auto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=100)),
                ('color', models.CharField(max_length=100)),
                ('production_year', models.IntegerField(blank=True, null=True)),
                ('engine_capacity', models.IntegerField(blank=True, null=True)),
                ('vin_code', models.IntegerField(unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Owner',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=128)),
                ('last_name', models.CharField(max_length=128)),
            ],
        ),
        migrations.CreateModel(
            name='OwnerAuto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.auto')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.owner')),
            ],
        ),
        migrations.AddField(
            model_name='auto',
            name='owners',
            field=models.ManyToManyField(through='api.OwnerAuto', to='api.Owner'),
        ),
    ]
