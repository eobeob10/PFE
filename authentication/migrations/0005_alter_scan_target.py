# Generated by Django 4.0.4 on 2022-05-27 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_scan_status_alter_scan_client_alter_scan_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scan',
            name='Target',
            field=models.FileField(upload_to='uploads/'),
        ),
    ]