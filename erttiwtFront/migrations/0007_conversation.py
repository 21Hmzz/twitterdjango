# Generated by Django 3.2.18 on 2023-06-07 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('erttiwtFront', '0006_merge_0003_auto_20230607_0941_0005_auto_20230605_1951'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('idConversation', models.AutoField(primary_key=True, serialize=False)),
                ('user1', models.IntegerField()),
                ('user2', models.IntegerField()),
            ],
        ),
    ]
