# Generated by Django 5.0.2 on 2024-09-23 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_module', '0010_alter_fighter_sex'),
    ]

    operations = [
        migrations.AddField(
            model_name='fighter',
            name='coach_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
