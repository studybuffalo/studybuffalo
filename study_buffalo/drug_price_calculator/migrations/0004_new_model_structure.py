from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ('drug_price_calculator', '0003_delete_old_models'),
    ]

    operations = [
        migrations.CreateModel(
            name='ATC',
            fields=[
                ('id', models.CharField(max_length=7, primary_key=True, serialize=False, unique=True)),
                ('atc_1', models.CharField(max_length=7, null=True)),
                ('atc_1_text', models.CharField(max_length=200, null=True)),
                ('atc_2', models.CharField(max_length=7, null=True)),
                ('atc_2_text', models.CharField(max_length=200, null=True)),
                ('atc_3', models.CharField(max_length=7, null=True)),
                ('atc_3_text', models.CharField(max_length=200, null=True)),
                ('atc_4', models.CharField(max_length=7, null=True)),
                ('atc_4_text', models.CharField(max_length=200, null=True)),
            ],
            options={
                'verbose_name': 'Anatomical Therapeutic Category',
                'verbose_name_plural': 'Anatomical Therapeutic Categories',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('group_1', models.BooleanField(default=False)),
                ('group_66', models.BooleanField(default=False)),
                ('group_19823', models.BooleanField(default=False)),
                ('group_19823a', models.BooleanField(default=False)),
                ('group_19824', models.BooleanField(default=False)),
                ('group_20400', models.BooleanField(default=False)),
                ('group_20403', models.BooleanField(default=False)),
                ('group_20514', models.BooleanField(default=False)),
                ('group_22128', models.BooleanField(default=False)),
                ('group_23609', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('din', models.CharField(help_text="The drug's DIN/NPN/PIN", max_length=8, unique=True)),
                ('brand_name', models.CharField(blank=True, help_text='The brand name or trade name', max_length=70, null=True)),
                ('strength', models.CharField(blank=True, help_text='The strength(s) of the medications', max_length=200, null=True)),
                ('route', models.CharField(blank=True, help_text='The route of administration', max_length=20, null=True)),
                ('dosage_form', models.CharField(blank=True, help_text='The dosage form', max_length=35, null=True)),
                ('generic_name', models.CharField(blank=True, help_text='The generic name', max_length=450, null=True)),
                ('manufacturer', models.CharField(blank=True, help_text='The drug manufacturer', max_length=75, null=True)),
                ('schedule', models.CharField(blank=True, help_text='The provincial drug schedule', max_length=10, null=True)),
                ('atc', models.ForeignKey(blank=True, help_text='The ATC code for this drug', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drugs', to='drug_price_calculator.ATC')),
            ],
        ),
        migrations.CreateModel(
            name='PTC',
            fields=[
                ('id', models.CharField(max_length=11, primary_key=True, serialize=False, unique=True)),
                ('ptc_1', models.CharField(max_length=11, null=True)),
                ('ptc_1_text', models.CharField(max_length=75, null=True)),
                ('ptc_2', models.CharField(max_length=11, null=True)),
                ('ptc_2_text', models.CharField(max_length=75, null=True)),
                ('ptc_3', models.CharField(max_length=11, null=True)),
                ('ptc_3_text', models.CharField(max_length=75, null=True)),
                ('ptc_4', models.CharField(max_length=11, null=True)),
                ('ptc_4_text', models.CharField(max_length=75, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialAuthorization',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(help_text='The name of the PDF file', max_length=15)),
                ('pdf_title', models.CharField(help_text='The tile of the PDF', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('abc_id', models.PositiveIntegerField(help_text='The Alberta Blue Cross iDBL ID number')),
                ('date_listed', models.DateField(blank=True, help_text='The date listed or date updated', null=True)),
                ('unit_price', models.DecimalField(blank=True, decimal_places=4, help_text='The unit price (in CAD)', max_digits=10, null=True)),
                ('lca_price', models.DecimalField(blank=True, decimal_places=4, help_text='The Least Cost Alternative price (in CAD)', max_digits=10, null=True)),
                ('mac_price', models.DecimalField(blank=True, decimal_places=4, help_text='The Maximum Allowable Cost price (in CAD)', max_digits=10, null=True)),
                ('mac_text', models.CharField(blank=True, help_text='Descriptions for the MAC pricing', max_length=150, null=True)),
                ('unit_issue', models.CharField(blank=True, help_text='The unit of issue for pricing', max_length=25, null=True)),
                ('interchangeable', models.BooleanField(default=False, help_text='Whether are interchangeable products or not')),
                ('coverage_status', models.CharField(blank=True, help_text='The coverage status of the drug', max_length=100, null=True)),
                ('date_added', models.DateTimeField(auto_now=True, help_text='The date and time this price was added')),
                ('clients', models.OneToOneField(blank=True, help_text='The details of which clients cover applies to', null=True, on_delete=django.db.models.deletion.SET_NULL, to='drug_price_calculator.Clients')),
                ('drug', models.ForeignKey(help_text='The drug this price applies to', on_delete=django.db.models.deletion.CASCADE, related_name='prices', to='drug_price_calculator.Drug')),
                ('special_authorizations', models.ManyToManyField(help_text='Special Authorization forms that apply to this drug', related_name='drugs', to='drug_price_calculator.SpecialAuthorization')),
            ],
        ),
        migrations.AddField(
            model_name='drug',
            name='ptc',
            field=models.ForeignKey(blank=True, help_text='The PTC code for this drug', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='drugs', to='drug_price_calculator.PTC'),
        ),
        migrations.CreateModel(
            name='CoverageCriteria',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('header', models.CharField(blank=True, help_text='Any header for this criteria', max_length=200, null=True)),
                ('criteria', models.TextField(help_text='The coverage criteria')),
                ('price', models.ForeignKey(help_text='The drug price this criteria applies to', on_delete=django.db.models.deletion.CASCADE, related_name='coverage_criteria', to='drug_price_calculator.Price')),
            ],
        ),
    ]
