# Generated by Django 5.0.6 on 2024-07-29 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0014_remove_custumer_alamat'),
    ]

    operations = [
        migrations.AddField(
            model_name='custumer',
            name='alamat',
            field=models.TextField(null=True),
        ),
    ]