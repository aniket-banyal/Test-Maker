# Generated by Django 3.1.7 on 2021-03-17 06:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='point',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]