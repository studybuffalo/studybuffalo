# Generated by Django 2.0.3 on 2018-05-29 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('flash_cards', '0017_auto_20180529_0920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='deckfeedback',
            old_name='Deck',
            new_name='deck',
        ),
    ]
