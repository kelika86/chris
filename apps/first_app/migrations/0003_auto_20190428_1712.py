# Generated by Django 2.1.1 on 2019-04-29 00:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0002_remove_ticket_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='buyer',
        ),
        migrations.AddField(
            model_name='order',
            name='buyers',
            field=models.ManyToManyField(related_name='bought_tickets', to='first_app.Ticket'),
        ),
    ]
