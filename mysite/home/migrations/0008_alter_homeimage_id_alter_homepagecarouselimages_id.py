# Generated by Django 4.2.5 on 2023-10-11 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("home", "0007_homepagecarouselimages"),
    ]

    operations = [
        migrations.AlterField(
            model_name="homeimage",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name="homepagecarouselimages",
            name="id",
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
