# Generated by Django 4.2.5 on 2023-09-20 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0089_log_entry_data_json_null_to_object'),
        ('scraper', '0002_formfield'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ResultsPage',
            new_name='UrlInputPageLanding',
        ),
    ]
