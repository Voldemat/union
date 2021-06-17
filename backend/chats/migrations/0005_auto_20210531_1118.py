# Generated by Django 3.2 on 2021-05-31 11:18

from django.conf import settings
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chats', '0004_alter_message_text'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chat',
            name='name',
            field=models.CharField(default='GroupChat', max_length=50),
        ),
        migrations.CreateModel(
            name='PersonalChat',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('users', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]