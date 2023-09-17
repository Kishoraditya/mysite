# Generated by Django 4.2.5 on 2023-09-16 20:38

from django.db import migrations
import wagtail.blocks
import wagtail.fields
import wagtail.images.blocks


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_blogtagindexpage_blogpagetag_blogpage_tags'),
    ]

    operations = [
    migrations.AlterField(
        model_name='blogpage',
        name='body',
        field=wagtail.fields.StreamField([('heading', wagtail.blocks.CharBlock(form_classname='title')), ('paragraph', wagtail.blocks.RichTextBlock()), ('image', wagtail.images.blocks.ImageChooserBlock())], use_json_field=True),
    ),
]
