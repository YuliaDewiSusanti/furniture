# Generated by Django 4.2.6 on 2024-06-30 07:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0007_rename_no_whatsup_kontak_telpon'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kontak',
            old_name='subject',
            new_name='subjek',
        ),
    ]