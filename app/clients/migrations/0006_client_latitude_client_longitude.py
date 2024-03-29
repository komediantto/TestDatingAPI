# Generated by Django 4.2 on 2023-06-29 13:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0005_alter_client_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='latitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='client',
            name='longitude',
            field=models.DecimalField(decimal_places=6, default=1, max_digits=9),
            preserve_default=False,
        ),
    ]
