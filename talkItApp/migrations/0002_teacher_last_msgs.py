# Generated by Django 4.2.2 on 2023-06-15 12:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("talkItApp", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="teacher",
            name="last_msgs",
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
    ]
