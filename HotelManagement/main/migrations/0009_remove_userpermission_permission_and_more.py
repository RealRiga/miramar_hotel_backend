# Generated by Django 5.0.4 on 2024-06-24 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_delete_inquiry_remove_feedback_user_feedback_email_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userpermission',
            name='permission',
        ),
        migrations.RemoveField(
            model_name='userpermission',
            name='user',
        ),
        migrations.AddField(
            model_name='room',
            name='availability',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='UserGroup',
        ),
        migrations.DeleteModel(
            name='UserPermission',
        ),
    ]
