# Generated by Django 5.1.7 on 2025-03-29 22:19

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chatbox', '0002_alter_chatmessage_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatmessage',
            name='chat_id',
            field=models.UUIDField(default=uuid.uuid4),
        ),
    ]
