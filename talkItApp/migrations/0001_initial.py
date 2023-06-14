# Generated by Django 4.1.3 on 2023-05-27 17:11

from django.db import migrations, models
import django.db.models.deletion
import talkItApp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=32)),
                ('email', models.CharField(max_length=32)),
                ('password', models.CharField(max_length=32)),
                ('apiCode', models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Teacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('gender', models.CharField(choices=[(talkItApp.models.Gender['MALE'], 'Male'), (talkItApp.models.Gender['FEMALE'], 'Female')], max_length=10)),
                ('prompt', models.CharField(blank=True, max_length=1024, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='talkItApp.user')),
            ],
        ),
    ]
