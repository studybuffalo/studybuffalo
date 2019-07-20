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
                (
                    'id',
                    models.CharField(
                        max_length=7,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    )
                ),
                (
                    'atc_1',
                    models.CharField(
                        blank=True,
                        max_length=7,
                        null=True,
                        verbose_name='ATC level 1 code',
                    )
                ),
                (
                    'atc_1_text',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name='ATC level 1 description',
                    )
                ),
                (
                    'atc_2',
                    models.CharField(
                        blank=True,
                        max_length=7,
                        null=True,
                        verbose_name='ATC level 2 code',
                    )
                ),
                (
                    'atc_2_text',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name='ATC level 2 description',
                    )
                ),
                (
                    'atc_3',
                    models.CharField(
                        blank=True,
                        max_length=7,
                        null=True,
                        verbose_name='ATC level 3 code',
                    )
                ),
                (
                    'atc_3_text',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name='ATC level 3 description',
                    )
                ),
                (
                    'atc_4',
                    models.CharField(
                        blank=True,
                        max_length=7,
                        null=True,
                        verbose_name='ATC level 4 code',
                    )
                ),
                (
                    'atc_4_text',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name='ATC level 4 description',
                    )
                ),
                (
                    'atc_5',
                    models.CharField(
                        blank=True,
                        max_length=7,
                        null=True,
                        verbose_name='ATC level 5 code',
                    )
                ),
                (
                    'atc_5_text',
                    models.CharField(
                        blank=True,
                        max_length=200,
                        null=True,
                        verbose_name='ATC level 5 description',
                    )
                ),
            ],
            options={
                'verbose_name': 'Anatomical Therapeutic Category',
                'verbose_name_plural': 'Anatomical Therapeutic Categories',
            },
        ),
        migrations.CreateModel(
            name='Drug',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'din',
                    models.CharField(
                        help_text="The drug's DIN/NPN/PIN",
                        max_length=8,
                        unique=True,
                        verbose_name='DIN',
                    )
                ),
                (
                    'brand_name',
                    models.CharField(
                        blank=True,
                        help_text='The brand name or trade name',
                        max_length=80,
                        null=True,
                    )
                ),
                (
                    'strength',
                    models.CharField(
                        blank=True,
                        help_text='The strength(s) of the medications',
                        max_length=250,
                        null=True,
                    )
                ),
                (
                    'route',
                    models.CharField(
                        blank=True,
                        help_text='The route of administration',
                        max_length=20,
                        null=True,
                    )
                ),
                (
                    'dosage_form',
                    models.CharField(
                        blank=True,
                        help_text='The dosage form',
                        max_length=40,
                        null=True,
                    )
                ),
                (
                    'generic_name',
                    models.CharField(
                        blank=True,
                        help_text='The generic name',
                        max_length=450,
                        null=True,
                    )
                ),
                (
                    'manufacturer',
                    models.CharField(
                        blank=True,
                        help_text='The drug manufacturer',
                        max_length=150,
                        null=True,
                    )
                ),
                (
                    'schedule',
                    models.CharField(
                        blank=True,
                        help_text='The provincial drug schedule',
                        max_length=10,
                        null=True,
                    )
                ),
                (
                    'generic_product',
                    models.CharField(
                        blank=True,
                        help_text='A calculated name to identify similar drugs',
                        max_length=750,
                        null=True,
                    )
                ),
                (
                    'atc',
                    models.ForeignKey(
                        blank=True,
                        help_text='The ATC code for this drug',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name='drugs',
                        to='drug_price_calculator.ATC',
                        verbose_name='ATC',
                    )
                ),
            ],
        ),
        migrations.CreateModel(
            name='PTC',
            fields=[
                (
                    'id',
                    models.CharField(
                        max_length=11,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    )
                ),
                (
                    'ptc_1',
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        verbose_name='PTC level 1 code',
                    )
                ),
                (
                    'ptc_1_text',
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name='PTC level 1 description',
                    )
                ),
                (
                    'ptc_2',
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        verbose_name='PTC level 2 code',
                    )
                ),
                (
                    'ptc_2_text',
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name='PTC level 2 description',
                    )
                ),
                (
                    'ptc_3',
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        verbose_name='PTC level 3 code',
                    )
                ),
                (
                    'ptc_3_text',
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name='PTC level 3 description',
                    )
                ),
                (
                    'ptc_4',
                    models.CharField(
                        blank=True,
                        max_length=11,
                        null=True,
                        verbose_name='PTC level 4 code',
                    )
                ),
                (
                    'ptc_4_text',
                    models.CharField(
                        blank=True,
                        max_length=100,
                        null=True,
                        verbose_name='PTC level 4 description',
                    )
                ),
            ],
            options={
                'verbose_name': 'Pharmacologic-Therapeutic Classification',
                'verbose_name_plural': 'Pharmacologic-Therapeutic Classifications',
            },
        ),
        migrations.CreateModel(
            name='SpecialAuthorization',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'file_name',
                    models.CharField(
                        help_text='The name of the PDF file',
                        max_length=15,
                    )
                ),
                (
                    'pdf_title',
                    models.CharField(
                        help_text='The tile of the PDF',
                        max_length=200,
                    )
                ),
            ],
        ),
        migrations.AlterModelOptions(
            name='pendbsrf',
            options={
                'verbose_name': 'Substitution - BSRF (Pending)',
                'verbose_name_plural': 'Substitutions - BSRF (Pending)'
            },
        ),
        migrations.AlterModelOptions(
            name='pendgeneric',
            options={
                'verbose_name': 'Substitution - Generic (Pending)',
                'verbose_name_plural': 'Substitutions - Generic (Pending)'
            },
        ),
        migrations.AlterModelOptions(
            name='pendmanufacturer',
            options={
                'verbose_name': 'Substitution - Manufactuer (Pending)',
                'verbose_name_plural': 'Substitutions - Manufactuer (Pending)'
            },
        ),
        migrations.AlterModelOptions(
            name='subsbsrf',
            options={
                'verbose_name': 'Substitution - BSRF',
                'verbose_name_plural': 'Substitutions - BSRF'
            },
        ),
        migrations.AlterModelOptions(
            name='subsgeneric',
            options={
                'verbose_name': 'Substitution - Generic',
                'verbose_name_plural': 'Substitutions - Generic'
            },
        ),
        migrations.AlterModelOptions(
            name='subsmanufacturer',
            options={
                'verbose_name': 'Substitution - Manufacturer',
                'verbose_name_plural': 'Substitutions - Manufacturer'
            },
        ),
        migrations.AlterModelOptions(
            name='subsunit',
            options={
                'verbose_name': 'Substitution - Unit',
                'verbose_name_plural': 'Substitutions - Unit'
            },
        ),
        migrations.RemoveField(
            model_name='subsbsrf',
            name='bsrf',
        ),
        migrations.AddField(
            model_name='subsbsrf',
            name='original',
            field=models.CharField(default='', max_length=400, unique=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='brand_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='dosage_form',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='original',
            field=models.CharField(max_length=400, unique=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='route',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='pendbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='pendgeneric',
            name='correction',
            field=models.CharField(blank=True, max_length=450, null=True),
        ),
        migrations.AlterField(
            model_name='pendmanufacturer',
            name='correction',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='brand_name',
            field=models.CharField(blank=True, max_length=80, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='dosage_form',
            field=models.CharField(blank=True, max_length=40, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='route',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='subsbsrf',
            name='strength',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AlterField(
            model_name='subsgeneric',
            name='correction',
            field=models.CharField(blank=True, max_length=450, null=True),
        ),
        migrations.AlterField(
            model_name='subsmanufacturer',
            name='correction',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='subsmanufacturer',
            name='original',
            field=models.CharField(max_length=150, unique=True),
        ),
        migrations.AlterField(
            model_name='subsunit',
            name='correction',
            field=models.CharField(blank=True, max_length=120, null=True),
        ),
        migrations.CreateModel(
            name='Price',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'abc_id',
                    models.PositiveIntegerField(
                        help_text='The Alberta Blue Cross iDBL ID number',
                        verbose_name='ABC ID',
                    )
                ),
                (
                    'date_listed',
                    models.DateField(
                        blank=True,
                        help_text='The date listed or date updated',
                        null=True,
                    )
                ),
                (
                    'unit_price',
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        help_text='The unit price (in CAD)',
                        max_digits=10,
                        null=True,
                    )
                ),
                (
                    'lca_price', models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        help_text='The Least Cost Alternative price (in CAD)',
                        max_digits=10,
                        null=True,
                        verbose_name='LCA price',
                    )
                ),
                (
                    'mac_price',
                    models.DecimalField(
                        blank=True,
                        decimal_places=4,
                        help_text='The Maximum Allowable Cost price (in CAD)',
                        max_digits=10,
                        null=True,
                        verbose_name='MAC price',
                    )
                ),
                (
                    'mac_text',
                    models.CharField(
                        blank=True,
                        help_text='Descriptions for the MAC pricing',
                        max_length=150,
                        null=True,
                        verbose_name='MAC text',
                    )
                ),
                (
                    'unit_issue',
                    models.CharField(
                        blank=True,
                        help_text='The unit of issue for pricing',
                        max_length=25,
                        null=True,
                        verbose_name='unit of issue',
                    )
                ),
                (
                    'interchangeable',
                    models.BooleanField(
                        default=False,
                        help_text='Whether are interchangeable products or not',
                    )
                ),
                (
                    'coverage_status',
                    models.CharField(
                        blank=True,
                        help_text='The coverage status of the drug',
                        max_length=100,
                        null=True,
                    )
                ),
                (
                    'date_added',
                    models.DateTimeField(
                        auto_now=True,
                        help_text='The date and time this price was added',
                    )
                ),
                (
                    'drug',
                    models.ForeignKey(
                        help_text='The drug this price applies to',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='prices',
                        to='drug_price_calculator.Drug',
                    )
                ),
                (
                    'special_authorizations',
                    models.ManyToManyField(
                        help_text='Special Authorization forms that apply to this drug',
                        related_name='drugs',
                        to='drug_price_calculator.SpecialAuthorization',
                    )
                ),
            ],
        ),
        migrations.AddField(
            model_name='drug',
            name='ptc',
            field=models.ForeignKey(
                blank=True,
                help_text='The PTC code for this drug',
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='drugs',
                to='drug_price_calculator.PTC',
                verbose_name='PTC',
            ),
        ),
        migrations.CreateModel(
            name='CoverageCriteria',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'header',
                    models.CharField(
                        blank=True,
                        help_text='Any header for this criteria',
                        max_length=200,
                        null=True,
                    )
                ),
                (
                    'criteria',
                    models.TextField(
                        help_text='The coverage criteria',
                    )
                ),
                (
                    'price',
                    models.ForeignKey(
                        help_text='The drug price this criteria applies to',
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name='coverage_criteria',
                        to='drug_price_calculator.Price',
                    )
                ),
            ],
            options={
                'verbose_name_plural': 'coverage criteria',
            },
        ),
        migrations.CreateModel(
            name='Clients',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    )
                ),
                (
                    'group_1',
                    models.BooleanField(default=False)
                ),
                (
                    'group_66',
                    models.BooleanField(default=False)
                ),
                (
                    'group_19823',
                    models.BooleanField(default=False)
                ),
                (
                    'group_19823a',
                    models.BooleanField(default=False)
                ),
                (
                    'group_19824',
                    models.BooleanField(default=False)
                ),
                (
                    'group_20400',
                    models.BooleanField(default=False)
                ),
                (
                    'group_20403',
                    models.BooleanField(default=False)
                ),
                (
                    'group_20514',
                    models.BooleanField(default=False)
                ),
                (
                    'group_22128',
                    models.BooleanField(default=False)
                ),
                (
                    'group_23609',
                    models.BooleanField(default=False)
                ),
                (
                    'price',
                    models.OneToOneField(
                        blank=True,
                        help_text='The price details these clients apply to',
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to='drug_price_calculator.Price',
                    )
                ),
            ],
            options={
                'verbose_name_plural': 'clients',
            },
        ),
        migrations.CreateModel(
            name='PendUnit',
            fields=[
                (
                    'id', models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID'
                    )
                ),
                (
                    'original',
                    models.CharField(
                        max_length=120,
                        unique=True
                    )
                ),
                (
                    'correction',
                    models.CharField(
                        blank=True,
                        max_length=120,
                        null=True
                    )
                ),
            ],
            options={
                'verbose_name': 'Substitution - Unit (Pending)',
                'verbose_name_plural': 'Substitutions - Unit (Pending)',
            },
        ),
    ]
