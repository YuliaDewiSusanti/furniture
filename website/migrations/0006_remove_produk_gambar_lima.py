# Generated by Django 4.2.6 on 2024-06-23 08:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0005_statis_map'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produk',
            name='gambar_lima',
        ),
    ]