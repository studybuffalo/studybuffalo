from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0007_adding_meta_options'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subsbsrf',
            old_name='bsrf',
            new_name='original',
        ),
    ]
