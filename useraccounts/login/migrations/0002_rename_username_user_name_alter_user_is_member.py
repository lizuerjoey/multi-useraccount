# Generated by Django 4.2.7 on 2023-12-05 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='username',
            new_name='name',
        ),
        migrations.AlterField(
            model_name='user',
            name='is_member',
            field=models.BooleanField(default=True),
        ),
    ]