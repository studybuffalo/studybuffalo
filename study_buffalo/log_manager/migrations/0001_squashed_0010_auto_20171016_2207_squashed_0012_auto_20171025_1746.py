# Generated by Django 2.0.3 on 2018-05-28 14:29

import datetime
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone


class Migration(migrations.Migration):

    replaces = [('log_manager', '0001_squashed_0010_auto_20171016_2207'), ('log_manager', '0002_auto_20171017_1616'), ('log_manager', '0003_auto_20171019_1749'), ('log_manager', '0004_auto_20171019_1800'), ('log_manager', '0005_remove_logentry_level_no'), ('log_manager', '0006_logentry_level_no'), ('log_manager', '0007_appdata_log_timezone'), ('log_manager', '0008_auto_20171022_1216'), ('log_manager', '0009_appdata_asc_time_format'), ('log_manager', '0010_auto_20171023_1804'), ('log_manager', '0011_auto_20171023_1939'), ('log_manager', '0012_auto_20171025_1746')]

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AppData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(help_text='Name of the application to be monitored', max_length=256)),
                ('log_location', models.CharField(help_text='Absolute directory containing the log file(s)', max_length=512)),
                ('file_name', models.CharField(help_text='Regex expression that matches the log file name(s)', max_length=512)),
                ('flag_start', models.CharField(blank=True, help_text='Text located in the log file that notes the application has started properly', max_length=512, null=True)),
                ('flag_end', models.CharField(blank=True, help_text='Text located in the log file that notes the application has finished properly', max_length=512, null=True)),
                ('review_minute', models.PositiveSmallIntegerField(blank=True, help_text='The minutes of an hour to update on', null=True, validators=[django.core.validators.MaxValueValidator(59)])),
                ('review_hour', models.PositiveSmallIntegerField(blank=True, help_text='The hour of the day to update on (0 = midnight)', null=True, validators=[django.core.validators.MaxValueValidator(59)])),
                ('review_day', models.PositiveSmallIntegerField(blank=True, help_text='The day of the month to update on (1-31)', null=True, validators=[django.core.validators.MaxValueValidator(59)])),
                ('review_month', models.PositiveSmallIntegerField(blank=True, help_text='The month to update on (1 = January, 12 = December)', null=True, validators=[django.core.validators.MaxValueValidator(59)])),
                ('review_weekday', models.PositiveSmallIntegerField(blank=True, help_text='The weekday to update on (0 = Sunday, 6 = Saturday)', null=True, validators=[django.core.validators.MaxValueValidator(6)])),
                ('next_review', models.DateTimeField(default=datetime.datetime(2017, 10, 16, 17, 37, 53, 589581))),
                ('last_reviewed_log', models.DateTimeField(default=datetime.datetime(2017, 10, 16, 17, 37, 53, 589581))),
                ('last_review', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('asc_time', models.DateTimeField(blank=True, null=True)),
                ('created', models.CharField(blank=True, max_length=25, null=True)),
                ('exc_info', models.TextField(blank=True, null=True)),
                ('file_name', models.CharField(blank=True, max_length=512, null=True)),
                ('func_name', models.CharField(blank=True, max_length=512, null=True)),
                ('level_name', models.CharField(blank=True, max_length=512, null=True)),
                ('line_no', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('module', models.CharField(blank=True, max_length=512, null=True)),
                ('msecs', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('message', models.TextField(blank=True, null=True)),
                ('name', models.CharField(blank=True, max_length=512, null=True)),
                ('path_name', models.CharField(blank=True, max_length=512, null=True)),
                ('process', models.CharField(blank=True, max_length=512, null=True)),
                ('process_name', models.CharField(blank=True, max_length=512, null=True)),
                ('relative_created', models.CharField(blank=True, max_length=25, null=True)),
                ('stack_info', models.TextField(blank=True, null=True)),
                ('thread', models.CharField(blank=True, max_length=512, null=True)),
                ('thread_name', models.CharField(blank=True, max_length=512, null=True)),
                ('app_name', models.ForeignKey(help_text='The app this entry is for', on_delete=django.db.models.deletion.CASCADE, to='log_manager.AppData')),
                ('level_no', models.PositiveSmallIntegerField(blank=True, null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 18, 31, 33, 690980)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 18, 31, 33, 690980)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 15, 14, 153622)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 15, 14, 153622)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 15, 51, 57655)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 15, 51, 57655)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 22, 5, 781126)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 19, 22, 5, 781126)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 20, 15, 1, 560050)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 20, 15, 1, 560050)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 20, 16, 20, 574434)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 20, 16, 20, 574434)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 21, 33, 40, 809961)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 16, 21, 33, 40, 809961)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 4, 6, 19, 360489, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 4, 6, 19, 360489, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 4, 7, 12, 177808, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=datetime.datetime(2017, 10, 17, 4, 7, 12, 177808, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='last_reviewed_log',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='next_review',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterModelOptions(
            name='appdata',
            options={'permissions': (('can_view', 'Can view the app log data'),)},
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_day',
            field=models.CharField(blank=True, default='*', help_text='The day of the month to update on (1-31)', max_length=100, null=True, validators=[django.core.validators.MaxValueValidator(59)]),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_hour',
            field=models.CharField(blank=True, default='*', help_text='The hour of the day to update on (0 = midnight)', max_length=100, null=True, validators=[django.core.validators.MaxValueValidator(59)]),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_minute',
            field=models.CharField(blank=True, default='*', help_text='The minutes of an hour to update on', max_length=100, null=True, validators=[django.core.validators.MaxValueValidator(59)]),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_month',
            field=models.CharField(blank=True, default='*', help_text='The month to update on (1 = January, 12 = December)', max_length=100, null=True, validators=[django.core.validators.MaxValueValidator(59)]),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_weekday',
            field=models.CharField(blank=True, default='*', help_text='The weekday to update on (0 = Sunday, 6 = Saturday)', max_length=100, null=True, validators=[django.core.validators.MaxValueValidator(6)]),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_day',
            field=models.CharField(blank=True, default='*', help_text='The day of the month to update on (1-31)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_hour',
            field=models.CharField(blank=True, default='*', help_text='The hour of the day to update on (0 = midnight)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_minute',
            field=models.CharField(blank=True, default='*', help_text='The minutes of an hour to update on', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_month',
            field=models.CharField(blank=True, default='*', help_text='The month to update on (1 = January, 12 = December)', max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='appdata',
            name='review_weekday',
            field=models.CharField(blank=True, default='*', help_text='The weekday to update on (0 = Sunday, 6 = Saturday)', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='appdata',
            name='log_timezone',
            field=models.CharField(blank=True, choices=[('Africa/Abidjan', 'Africa/Abidjan'), ('Africa/Accra', 'Africa/Accra'), ('Africa/Addis_Ababa', 'Africa/Addis_Ababa'), ('Africa/Algiers', 'Africa/Algiers'), ('Africa/Asmara', 'Africa/Asmara'), ('Africa/Bamako', 'Africa/Bamako'), ('Africa/Bangui', 'Africa/Bangui'), ('Africa/Banjul', 'Africa/Banjul'), ('Africa/Bissau', 'Africa/Bissau'), ('Africa/Blantyre', 'Africa/Blantyre'), ('Africa/Brazzaville', 'Africa/Brazzaville'), ('Africa/Bujumbura', 'Africa/Bujumbura'), ('Africa/Cairo', 'Africa/Cairo'), ('Africa/Casablanca', 'Africa/Casablanca'), ('Africa/Ceuta', 'Africa/Ceuta'), ('Africa/Conakry', 'Africa/Conakry'), ('Africa/Dakar', 'Africa/Dakar'), ('Africa/Dar_es_Salaam', 'Africa/Dar_es_Salaam'), ('Africa/Djibouti', 'Africa/Djibouti'), ('Africa/Douala', 'Africa/Douala'), ('Africa/El_Aaiun', 'Africa/El_Aaiun'), ('Africa/Freetown', 'Africa/Freetown'), ('Africa/Gaborone', 'Africa/Gaborone'), ('Africa/Harare', 'Africa/Harare'), ('Africa/Johannesburg', 'Africa/Johannesburg'), ('Africa/Juba', 'Africa/Juba'), ('Africa/Kampala', 'Africa/Kampala'), ('Africa/Khartoum', 'Africa/Khartoum'), ('Africa/Kigali', 'Africa/Kigali'), ('Africa/Kinshasa', 'Africa/Kinshasa'), ('Africa/Lagos', 'Africa/Lagos'), ('Africa/Libreville', 'Africa/Libreville'), ('Africa/Lome', 'Africa/Lome'), ('Africa/Luanda', 'Africa/Luanda'), ('Africa/Lubumbashi', 'Africa/Lubumbashi'), ('Africa/Lusaka', 'Africa/Lusaka'), ('Africa/Malabo', 'Africa/Malabo'), ('Africa/Maputo', 'Africa/Maputo'), ('Africa/Maseru', 'Africa/Maseru'), ('Africa/Mbabane', 'Africa/Mbabane'), ('Africa/Mogadishu', 'Africa/Mogadishu'), ('Africa/Monrovia', 'Africa/Monrovia'), ('Africa/Nairobi', 'Africa/Nairobi'), ('Africa/Ndjamena', 'Africa/Ndjamena'), ('Africa/Niamey', 'Africa/Niamey'), ('Africa/Nouakchott', 'Africa/Nouakchott'), ('Africa/Ouagadougou', 'Africa/Ouagadougou'), ('Africa/Porto-Novo', 'Africa/Porto-Novo'), ('Africa/Sao_Tome', 'Africa/Sao_Tome'), ('Africa/Tripoli', 'Africa/Tripoli'), ('Africa/Tunis', 'Africa/Tunis'), ('Africa/Windhoek', 'Africa/Windhoek'), ('America/Adak', 'America/Adak'), ('America/Anchorage', 'America/Anchorage'), ('America/Anguilla', 'America/Anguilla'), ('America/Antigua', 'America/Antigua'), ('America/Araguaina', 'America/Araguaina'), ('America/Argentina/Buenos_Aires', 'America/Argentina/Buenos_Aires'), ('America/Argentina/Catamarca', 'America/Argentina/Catamarca'), ('America/Argentina/Cordoba', 'America/Argentina/Cordoba'), ('America/Argentina/Jujuy', 'America/Argentina/Jujuy'), ('America/Argentina/La_Rioja', 'America/Argentina/La_Rioja'), ('America/Argentina/Mendoza', 'America/Argentina/Mendoza'), ('America/Argentina/Rio_Gallegos', 'America/Argentina/Rio_Gallegos'), ('America/Argentina/Salta', 'America/Argentina/Salta'), ('America/Argentina/San_Juan', 'America/Argentina/San_Juan'), ('America/Argentina/San_Luis', 'America/Argentina/San_Luis'), ('America/Argentina/Tucuman', 'America/Argentina/Tucuman'), ('America/Argentina/Ushuaia', 'America/Argentina/Ushuaia'), ('America/Aruba', 'America/Aruba'), ('America/Asuncion', 'America/Asuncion'), ('America/Atikokan', 'America/Atikokan'), ('America/Bahia', 'America/Bahia'), ('America/Bahia_Banderas', 'America/Bahia_Banderas'), ('America/Barbados', 'America/Barbados'), ('America/Belem', 'America/Belem'), ('America/Belize', 'America/Belize'), ('America/Blanc-Sablon', 'America/Blanc-Sablon'), ('America/Boa_Vista', 'America/Boa_Vista'), ('America/Bogota', 'America/Bogota'), ('America/Boise', 'America/Boise'), ('America/Cambridge_Bay', 'America/Cambridge_Bay'), ('America/Campo_Grande', 'America/Campo_Grande'), ('America/Cancun', 'America/Cancun'), ('America/Caracas', 'America/Caracas'), ('America/Cayenne', 'America/Cayenne'), ('America/Cayman', 'America/Cayman'), ('America/Chicago', 'America/Chicago'), ('America/Chihuahua', 'America/Chihuahua'), ('America/Costa_Rica', 'America/Costa_Rica'), ('America/Creston', 'America/Creston'), ('America/Cuiaba', 'America/Cuiaba'), ('America/Curacao', 'America/Curacao'), ('America/Danmarkshavn', 'America/Danmarkshavn'), ('America/Dawson', 'America/Dawson'), ('America/Dawson_Creek', 'America/Dawson_Creek'), ('America/Denver', 'America/Denver'), ('America/Detroit', 'America/Detroit'), ('America/Dominica', 'America/Dominica'), ('America/Edmonton', 'America/Edmonton'), ('America/Eirunepe', 'America/Eirunepe'), ('America/El_Salvador', 'America/El_Salvador'), ('America/Fort_Nelson', 'America/Fort_Nelson'), ('America/Fortaleza', 'America/Fortaleza'), ('America/Glace_Bay', 'America/Glace_Bay'), ('America/Godthab', 'America/Godthab'), ('America/Goose_Bay', 'America/Goose_Bay'), ('America/Grand_Turk', 'America/Grand_Turk'), ('America/Grenada', 'America/Grenada'), ('America/Guadeloupe', 'America/Guadeloupe'), ('America/Guatemala', 'America/Guatemala'), ('America/Guayaquil', 'America/Guayaquil'), ('America/Guyana', 'America/Guyana'), ('America/Halifax', 'America/Halifax'), ('America/Havana', 'America/Havana'), ('America/Hermosillo', 'America/Hermosillo'), ('America/Indiana/Indianapolis', 'America/Indiana/Indianapolis'), ('America/Indiana/Knox', 'America/Indiana/Knox'), ('America/Indiana/Marengo', 'America/Indiana/Marengo'), ('America/Indiana/Petersburg', 'America/Indiana/Petersburg'), ('America/Indiana/Tell_City', 'America/Indiana/Tell_City'), ('America/Indiana/Vevay', 'America/Indiana/Vevay'), ('America/Indiana/Vincennes', 'America/Indiana/Vincennes'), ('America/Indiana/Winamac', 'America/Indiana/Winamac'), ('America/Inuvik', 'America/Inuvik'), ('America/Iqaluit', 'America/Iqaluit'), ('America/Jamaica', 'America/Jamaica'), ('America/Juneau', 'America/Juneau'), ('America/Kentucky/Louisville', 'America/Kentucky/Louisville'), ('America/Kentucky/Monticello', 'America/Kentucky/Monticello'), ('America/Kralendijk', 'America/Kralendijk'), ('America/La_Paz', 'America/La_Paz'), ('America/Lima', 'America/Lima'), ('America/Los_Angeles', 'America/Los_Angeles'), ('America/Lower_Princes', 'America/Lower_Princes'), ('America/Maceio', 'America/Maceio'), ('America/Managua', 'America/Managua'), ('America/Manaus', 'America/Manaus'), ('America/Marigot', 'America/Marigot'), ('America/Martinique', 'America/Martinique'), ('America/Matamoros', 'America/Matamoros'), ('America/Mazatlan', 'America/Mazatlan'), ('America/Menominee', 'America/Menominee'), ('America/Merida', 'America/Merida'), ('America/Metlakatla', 'America/Metlakatla'), ('America/Mexico_City', 'America/Mexico_City'), ('America/Miquelon', 'America/Miquelon'), ('America/Moncton', 'America/Moncton'), ('America/Monterrey', 'America/Monterrey'), ('America/Montevideo', 'America/Montevideo'), ('America/Montserrat', 'America/Montserrat'), ('America/Nassau', 'America/Nassau'), ('America/New_York', 'America/New_York'), ('America/Nipigon', 'America/Nipigon'), ('America/Nome', 'America/Nome'), ('America/Noronha', 'America/Noronha'), ('America/North_Dakota/Beulah', 'America/North_Dakota/Beulah'), ('America/North_Dakota/Center', 'America/North_Dakota/Center'), ('America/North_Dakota/New_Salem', 'America/North_Dakota/New_Salem'), ('America/Ojinaga', 'America/Ojinaga'), ('America/Panama', 'America/Panama'), ('America/Pangnirtung', 'America/Pangnirtung'), ('America/Paramaribo', 'America/Paramaribo'), ('America/Phoenix', 'America/Phoenix'), ('America/Port-au-Prince', 'America/Port-au-Prince'), ('America/Port_of_Spain', 'America/Port_of_Spain'), ('America/Porto_Velho', 'America/Porto_Velho'), ('America/Puerto_Rico', 'America/Puerto_Rico'), ('America/Punta_Arenas', 'America/Punta_Arenas'), ('America/Rainy_River', 'America/Rainy_River'), ('America/Rankin_Inlet', 'America/Rankin_Inlet'), ('America/Recife', 'America/Recife'), ('America/Regina', 'America/Regina'), ('America/Resolute', 'America/Resolute'), ('America/Rio_Branco', 'America/Rio_Branco'), ('America/Santarem', 'America/Santarem'), ('America/Santiago', 'America/Santiago'), ('America/Santo_Domingo', 'America/Santo_Domingo'), ('America/Sao_Paulo', 'America/Sao_Paulo'), ('America/Scoresbysund', 'America/Scoresbysund'), ('America/Sitka', 'America/Sitka'), ('America/St_Barthelemy', 'America/St_Barthelemy'), ('America/St_Johns', 'America/St_Johns'), ('America/St_Kitts', 'America/St_Kitts'), ('America/St_Lucia', 'America/St_Lucia'), ('America/St_Thomas', 'America/St_Thomas'), ('America/St_Vincent', 'America/St_Vincent'), ('America/Swift_Current', 'America/Swift_Current'), ('America/Tegucigalpa', 'America/Tegucigalpa'), ('America/Thule', 'America/Thule'), ('America/Thunder_Bay', 'America/Thunder_Bay'), ('America/Tijuana', 'America/Tijuana'), ('America/Toronto', 'America/Toronto'), ('America/Tortola', 'America/Tortola'), ('America/Vancouver', 'America/Vancouver'), ('America/Whitehorse', 'America/Whitehorse'), ('America/Winnipeg', 'America/Winnipeg'), ('America/Yakutat', 'America/Yakutat'), ('America/Yellowknife', 'America/Yellowknife'), ('Antarctica/Casey', 'Antarctica/Casey'), ('Antarctica/Davis', 'Antarctica/Davis'), ('Antarctica/DumontDUrville', 'Antarctica/DumontDUrville'), ('Antarctica/Macquarie', 'Antarctica/Macquarie'), ('Antarctica/Mawson', 'Antarctica/Mawson'), ('Antarctica/McMurdo', 'Antarctica/McMurdo'), ('Antarctica/Palmer', 'Antarctica/Palmer'), ('Antarctica/Rothera', 'Antarctica/Rothera'), ('Antarctica/Syowa', 'Antarctica/Syowa'), ('Antarctica/Troll', 'Antarctica/Troll'), ('Antarctica/Vostok', 'Antarctica/Vostok'), ('Arctic/Longyearbyen', 'Arctic/Longyearbyen'), ('Asia/Aden', 'Asia/Aden'), ('Asia/Almaty', 'Asia/Almaty'), ('Asia/Amman', 'Asia/Amman'), ('Asia/Anadyr', 'Asia/Anadyr'), ('Asia/Aqtau', 'Asia/Aqtau'), ('Asia/Aqtobe', 'Asia/Aqtobe'), ('Asia/Ashgabat', 'Asia/Ashgabat'), ('Asia/Atyrau', 'Asia/Atyrau'), ('Asia/Baghdad', 'Asia/Baghdad'), ('Asia/Bahrain', 'Asia/Bahrain'), ('Asia/Baku', 'Asia/Baku'), ('Asia/Bangkok', 'Asia/Bangkok'), ('Asia/Barnaul', 'Asia/Barnaul'), ('Asia/Beirut', 'Asia/Beirut'), ('Asia/Bishkek', 'Asia/Bishkek'), ('Asia/Brunei', 'Asia/Brunei'), ('Asia/Chita', 'Asia/Chita'), ('Asia/Choibalsan', 'Asia/Choibalsan'), ('Asia/Colombo', 'Asia/Colombo'), ('Asia/Damascus', 'Asia/Damascus'), ('Asia/Dhaka', 'Asia/Dhaka'), ('Asia/Dili', 'Asia/Dili'), ('Asia/Dubai', 'Asia/Dubai'), ('Asia/Dushanbe', 'Asia/Dushanbe'), ('Asia/Famagusta', 'Asia/Famagusta'), ('Asia/Gaza', 'Asia/Gaza'), ('Asia/Hebron', 'Asia/Hebron'), ('Asia/Ho_Chi_Minh', 'Asia/Ho_Chi_Minh'), ('Asia/Hong_Kong', 'Asia/Hong_Kong'), ('Asia/Hovd', 'Asia/Hovd'), ('Asia/Irkutsk', 'Asia/Irkutsk'), ('Asia/Jakarta', 'Asia/Jakarta'), ('Asia/Jayapura', 'Asia/Jayapura'), ('Asia/Jerusalem', 'Asia/Jerusalem'), ('Asia/Kabul', 'Asia/Kabul'), ('Asia/Kamchatka', 'Asia/Kamchatka'), ('Asia/Karachi', 'Asia/Karachi'), ('Asia/Kathmandu', 'Asia/Kathmandu'), ('Asia/Khandyga', 'Asia/Khandyga'), ('Asia/Kolkata', 'Asia/Kolkata'), ('Asia/Krasnoyarsk', 'Asia/Krasnoyarsk'), ('Asia/Kuala_Lumpur', 'Asia/Kuala_Lumpur'), ('Asia/Kuching', 'Asia/Kuching'), ('Asia/Kuwait', 'Asia/Kuwait'), ('Asia/Macau', 'Asia/Macau'), ('Asia/Magadan', 'Asia/Magadan'), ('Asia/Makassar', 'Asia/Makassar'), ('Asia/Manila', 'Asia/Manila'), ('Asia/Muscat', 'Asia/Muscat'), ('Asia/Nicosia', 'Asia/Nicosia'), ('Asia/Novokuznetsk', 'Asia/Novokuznetsk'), ('Asia/Novosibirsk', 'Asia/Novosibirsk'), ('Asia/Omsk', 'Asia/Omsk'), ('Asia/Oral', 'Asia/Oral'), ('Asia/Phnom_Penh', 'Asia/Phnom_Penh'), ('Asia/Pontianak', 'Asia/Pontianak'), ('Asia/Pyongyang', 'Asia/Pyongyang'), ('Asia/Qatar', 'Asia/Qatar'), ('Asia/Qyzylorda', 'Asia/Qyzylorda'), ('Asia/Riyadh', 'Asia/Riyadh'), ('Asia/Sakhalin', 'Asia/Sakhalin'), ('Asia/Samarkand', 'Asia/Samarkand'), ('Asia/Seoul', 'Asia/Seoul'), ('Asia/Shanghai', 'Asia/Shanghai'), ('Asia/Singapore', 'Asia/Singapore'), ('Asia/Srednekolymsk', 'Asia/Srednekolymsk'), ('Asia/Taipei', 'Asia/Taipei'), ('Asia/Tashkent', 'Asia/Tashkent'), ('Asia/Tbilisi', 'Asia/Tbilisi'), ('Asia/Tehran', 'Asia/Tehran'), ('Asia/Thimphu', 'Asia/Thimphu'), ('Asia/Tokyo', 'Asia/Tokyo'), ('Asia/Tomsk', 'Asia/Tomsk'), ('Asia/Ulaanbaatar', 'Asia/Ulaanbaatar'), ('Asia/Urumqi', 'Asia/Urumqi'), ('Asia/Ust-Nera', 'Asia/Ust-Nera'), ('Asia/Vientiane', 'Asia/Vientiane'), ('Asia/Vladivostok', 'Asia/Vladivostok'), ('Asia/Yakutsk', 'Asia/Yakutsk'), ('Asia/Yangon', 'Asia/Yangon'), ('Asia/Yekaterinburg', 'Asia/Yekaterinburg'), ('Asia/Yerevan', 'Asia/Yerevan'), ('Atlantic/Azores', 'Atlantic/Azores'), ('Atlantic/Bermuda', 'Atlantic/Bermuda'), ('Atlantic/Canary', 'Atlantic/Canary'), ('Atlantic/Cape_Verde', 'Atlantic/Cape_Verde'), ('Atlantic/Faroe', 'Atlantic/Faroe'), ('Atlantic/Madeira', 'Atlantic/Madeira'), ('Atlantic/Reykjavik', 'Atlantic/Reykjavik'), ('Atlantic/South_Georgia', 'Atlantic/South_Georgia'), ('Atlantic/St_Helena', 'Atlantic/St_Helena'), ('Atlantic/Stanley', 'Atlantic/Stanley'), ('Australia/Adelaide', 'Australia/Adelaide'), ('Australia/Brisbane', 'Australia/Brisbane'), ('Australia/Broken_Hill', 'Australia/Broken_Hill'), ('Australia/Currie', 'Australia/Currie'), ('Australia/Darwin', 'Australia/Darwin'), ('Australia/Eucla', 'Australia/Eucla'), ('Australia/Hobart', 'Australia/Hobart'), ('Australia/Lindeman', 'Australia/Lindeman'), ('Australia/Lord_Howe', 'Australia/Lord_Howe'), ('Australia/Melbourne', 'Australia/Melbourne'), ('Australia/Perth', 'Australia/Perth'), ('Australia/Sydney', 'Australia/Sydney'), ('Canada/Atlantic', 'Canada/Atlantic'), ('Canada/Central', 'Canada/Central'), ('Canada/Eastern', 'Canada/Eastern'), ('Canada/Mountain', 'Canada/Mountain'), ('Canada/Newfoundland', 'Canada/Newfoundland'), ('Canada/Pacific', 'Canada/Pacific'), ('Europe/Amsterdam', 'Europe/Amsterdam'), ('Europe/Andorra', 'Europe/Andorra'), ('Europe/Astrakhan', 'Europe/Astrakhan'), ('Europe/Athens', 'Europe/Athens'), ('Europe/Belgrade', 'Europe/Belgrade'), ('Europe/Berlin', 'Europe/Berlin'), ('Europe/Bratislava', 'Europe/Bratislava'), ('Europe/Brussels', 'Europe/Brussels'), ('Europe/Bucharest', 'Europe/Bucharest'), ('Europe/Budapest', 'Europe/Budapest'), ('Europe/Busingen', 'Europe/Busingen'), ('Europe/Chisinau', 'Europe/Chisinau'), ('Europe/Copenhagen', 'Europe/Copenhagen'), ('Europe/Dublin', 'Europe/Dublin'), ('Europe/Gibraltar', 'Europe/Gibraltar'), ('Europe/Guernsey', 'Europe/Guernsey'), ('Europe/Helsinki', 'Europe/Helsinki'), ('Europe/Isle_of_Man', 'Europe/Isle_of_Man'), ('Europe/Istanbul', 'Europe/Istanbul'), ('Europe/Jersey', 'Europe/Jersey'), ('Europe/Kaliningrad', 'Europe/Kaliningrad'), ('Europe/Kiev', 'Europe/Kiev'), ('Europe/Kirov', 'Europe/Kirov'), ('Europe/Lisbon', 'Europe/Lisbon'), ('Europe/Ljubljana', 'Europe/Ljubljana'), ('Europe/London', 'Europe/London'), ('Europe/Luxembourg', 'Europe/Luxembourg'), ('Europe/Madrid', 'Europe/Madrid'), ('Europe/Malta', 'Europe/Malta'), ('Europe/Mariehamn', 'Europe/Mariehamn'), ('Europe/Minsk', 'Europe/Minsk'), ('Europe/Monaco', 'Europe/Monaco'), ('Europe/Moscow', 'Europe/Moscow'), ('Europe/Oslo', 'Europe/Oslo'), ('Europe/Paris', 'Europe/Paris'), ('Europe/Podgorica', 'Europe/Podgorica'), ('Europe/Prague', 'Europe/Prague'), ('Europe/Riga', 'Europe/Riga'), ('Europe/Rome', 'Europe/Rome'), ('Europe/Samara', 'Europe/Samara'), ('Europe/San_Marino', 'Europe/San_Marino'), ('Europe/Sarajevo', 'Europe/Sarajevo'), ('Europe/Saratov', 'Europe/Saratov'), ('Europe/Simferopol', 'Europe/Simferopol'), ('Europe/Skopje', 'Europe/Skopje'), ('Europe/Sofia', 'Europe/Sofia'), ('Europe/Stockholm', 'Europe/Stockholm'), ('Europe/Tallinn', 'Europe/Tallinn'), ('Europe/Tirane', 'Europe/Tirane'), ('Europe/Ulyanovsk', 'Europe/Ulyanovsk'), ('Europe/Uzhgorod', 'Europe/Uzhgorod'), ('Europe/Vaduz', 'Europe/Vaduz'), ('Europe/Vatican', 'Europe/Vatican'), ('Europe/Vienna', 'Europe/Vienna'), ('Europe/Vilnius', 'Europe/Vilnius'), ('Europe/Volgograd', 'Europe/Volgograd'), ('Europe/Warsaw', 'Europe/Warsaw'), ('Europe/Zagreb', 'Europe/Zagreb'), ('Europe/Zaporozhye', 'Europe/Zaporozhye'), ('Europe/Zurich', 'Europe/Zurich'), ('GMT', 'GMT'), ('Indian/Antananarivo', 'Indian/Antananarivo'), ('Indian/Chagos', 'Indian/Chagos'), ('Indian/Christmas', 'Indian/Christmas'), ('Indian/Cocos', 'Indian/Cocos'), ('Indian/Comoro', 'Indian/Comoro'), ('Indian/Kerguelen', 'Indian/Kerguelen'), ('Indian/Mahe', 'Indian/Mahe'), ('Indian/Maldives', 'Indian/Maldives'), ('Indian/Mauritius', 'Indian/Mauritius'), ('Indian/Mayotte', 'Indian/Mayotte'), ('Indian/Reunion', 'Indian/Reunion'), ('Pacific/Apia', 'Pacific/Apia'), ('Pacific/Auckland', 'Pacific/Auckland'), ('Pacific/Bougainville', 'Pacific/Bougainville'), ('Pacific/Chatham', 'Pacific/Chatham'), ('Pacific/Chuuk', 'Pacific/Chuuk'), ('Pacific/Easter', 'Pacific/Easter'), ('Pacific/Efate', 'Pacific/Efate'), ('Pacific/Enderbury', 'Pacific/Enderbury'), ('Pacific/Fakaofo', 'Pacific/Fakaofo'), ('Pacific/Fiji', 'Pacific/Fiji'), ('Pacific/Funafuti', 'Pacific/Funafuti'), ('Pacific/Galapagos', 'Pacific/Galapagos'), ('Pacific/Gambier', 'Pacific/Gambier'), ('Pacific/Guadalcanal', 'Pacific/Guadalcanal'), ('Pacific/Guam', 'Pacific/Guam'), ('Pacific/Honolulu', 'Pacific/Honolulu'), ('Pacific/Kiritimati', 'Pacific/Kiritimati'), ('Pacific/Kosrae', 'Pacific/Kosrae'), ('Pacific/Kwajalein', 'Pacific/Kwajalein'), ('Pacific/Majuro', 'Pacific/Majuro'), ('Pacific/Marquesas', 'Pacific/Marquesas'), ('Pacific/Midway', 'Pacific/Midway'), ('Pacific/Nauru', 'Pacific/Nauru'), ('Pacific/Niue', 'Pacific/Niue'), ('Pacific/Norfolk', 'Pacific/Norfolk'), ('Pacific/Noumea', 'Pacific/Noumea'), ('Pacific/Pago_Pago', 'Pacific/Pago_Pago'), ('Pacific/Palau', 'Pacific/Palau'), ('Pacific/Pitcairn', 'Pacific/Pitcairn'), ('Pacific/Pohnpei', 'Pacific/Pohnpei'), ('Pacific/Port_Moresby', 'Pacific/Port_Moresby'), ('Pacific/Rarotonga', 'Pacific/Rarotonga'), ('Pacific/Saipan', 'Pacific/Saipan'), ('Pacific/Tahiti', 'Pacific/Tahiti'), ('Pacific/Tarawa', 'Pacific/Tarawa'), ('Pacific/Tongatapu', 'Pacific/Tongatapu'), ('Pacific/Wake', 'Pacific/Wake'), ('Pacific/Wallis', 'Pacific/Wallis'), ('US/Alaska', 'US/Alaska'), ('US/Arizona', 'US/Arizona'), ('US/Central', 'US/Central'), ('US/Eastern', 'US/Eastern'), ('US/Hawaii', 'US/Hawaii'), ('US/Mountain', 'US/Mountain'), ('US/Pacific', 'US/Pacific'), ('UTC', 'UTC')], help_text='What timezone this log file uses for times', max_length=35, null=True),
        ),
        migrations.AddField(
            model_name='appdata',
            name='asc_time_format',
            field=models.CharField(default='Y-m-d H:M:S,f', help_text='The format of the asc_time field', max_length=50),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='appdata',
            name='flag_end',
        ),
        migrations.RemoveField(
            model_name='appdata',
            name='flag_start',
        ),
        migrations.AddField(
            model_name='appdata',
            name='monitor_start',
            field=models.BooleanField(default=False, help_text='Whether to notify the user or not if there are no new logentries when the log monitor checks at the specified time'),
        ),
    ]
