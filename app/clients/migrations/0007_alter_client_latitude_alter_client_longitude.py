# Generated by Django 4.2 on 2023-06-30 08:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0006_client_latitude_client_longitude'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='latitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AlterField(
            model_name='client',
            name='longitude',
            field=models.DecimalField(decimal_places=6, max_digits=9, null=True),
        ),
    ]
