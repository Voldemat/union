# Generated by Django 3.2 on 2021-07-04 18:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0008_auto_20210623_1124'),
    ]

    operations = [
        migrations.CreateModel(
            name='InviteToken',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('updated_at', models.DateTimeField(auto_now_add=True)),
                ('expired_at', models.DateTimeField()),
                ('user_invited', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='not_my_invite', to=settings.AUTH_USER_MODEL)),
                ('user_inviting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_invite', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]