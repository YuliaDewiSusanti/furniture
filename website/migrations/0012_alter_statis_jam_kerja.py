# Generated by Django 5.0.6 on 2024-07-02 06:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0011_statis_instagram_statis_jam_kerja_statis_whatsapp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statis',
            name='jam_kerja',
            field=models.CharField(max_length=200, null=True),
        ),
    ]