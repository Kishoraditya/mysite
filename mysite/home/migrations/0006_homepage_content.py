# Generated by Django 4.2.5 on 2023-09-25 19:53

from django.db import migrations
import wagtail.blocks
import wagtail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_remove_homepage_banner_cta_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='content',
            field=wagtail.fields.StreamField([('cta', wagtail.blocks.StructBlock([('title', wagtail.blocks.CharBlock(max_length=60, required=True)), ('text', wagtail.blocks.RichTextBlock(features=['bold', 'italic'], required=True)), ('button_page', wagtail.blocks.PageChooserBlock(required=False)), ('button_url', wagtail.blocks.URLBlock(required=False)), ('button_text', wagtail.blocks.CharBlock(default='Learn More', max_length=40, required=True))]))], blank=True, null=True, use_json_field=True),
        ),
    ]