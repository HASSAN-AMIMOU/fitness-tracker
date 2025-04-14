# Generated by Django 5.2 on 2025-04-14 18:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activities', '0003_alter_activity_user'),
    ]

    operations = [
    ]



def set_default_user(apps, schema_editor):
    Activity = apps.get_model('activities', 'Activity')
    User = apps.get_model('auth', 'User')
    default_user = User.objects.get(username='hassan')  # Change to your admin username
    Activity.objects.filter(user__isnull=True).update(user=default_user)

class Migration(migrations.Migration):
    dependencies = [
        ('activities', '0004_populate_user_field.py'),  # Replace with actual previous migration
    ]

    operations = [
        migrations.RunPython(set_default_user),
    ]