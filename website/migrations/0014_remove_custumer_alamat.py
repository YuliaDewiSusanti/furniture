# Generated by Django 5.0.6 on 2024-07-29 15:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0013_remove_statis_instagram_remove_statis_jam_kerja_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='custumer',
            name='alamat',
        ),
    ]