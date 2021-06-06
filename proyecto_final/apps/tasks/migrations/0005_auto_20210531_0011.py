# Generated by Django 2.2.4 on 2021-05-31 00:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0004_like'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='task',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='tasks.Task'),
        ),
        migrations.AlterField(
            model_name='like',
            name='users',
            field=models.ManyToManyField(related_name='likes', to='tasks.User'),
        ),
    ]
