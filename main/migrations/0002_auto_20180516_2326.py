# Generated by Django 2.0 on 2018-05-16 15:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Article',
        ),
        migrations.AlterModelOptions(
            name='alarm',
            options={'ordering': ['-alarm_id']},
        ),
        migrations.AddField(
            model_name='alarm',
            name='date_time',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
