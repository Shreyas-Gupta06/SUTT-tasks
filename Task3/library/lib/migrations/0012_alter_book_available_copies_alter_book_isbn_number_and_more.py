# Generated by Django 5.1.3 on 2025-01-08 07:00

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lib', '0011_borrowedhistory'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='available_copies',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='book',
            name='isbn_number',
            field=models.BigIntegerField(unique=True),
        ),
        migrations.AlterField(
            model_name='librarianprofile',
            name='psrn_number',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
