# Generated by Django 3.2 on 2021-05-12 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='text',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
