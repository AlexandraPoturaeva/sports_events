# Generated by Django 4.2.6 on 2023-11-19 11:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_application_participant'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='application',
            options={'get_latest_by': 'created_at', 'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='participant',
            options={'get_latest_by': 'created_at', 'ordering': ['last_name']},
        ),
    ]
