# Generated by Django 2.2.4 on 2021-05-30 23:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_auto_20210527_0039'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='liked_task', to='tasks.Task')),
                ('users', models.ManyToManyField(related_name='liked_by', to='tasks.User')),
            ],
        ),
    ]
