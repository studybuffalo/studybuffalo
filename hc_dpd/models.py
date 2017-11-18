from django.db import models

# Create your models here.
"""
    Database tables from original MySQL DB + new DPD files
"""
"""
ACTIVE_INGREDIENTS
	drug_code					int(8)
	active_ingredient_code		varchar(6)
	ingredient					varchar(240)
	ingredient_supplied_ind		varchar(1)
	strength					varchar(20)
	strength_unit				varchar(40)
	strength_type				varchar(40)
	dosage_value				varchar(20)
	base						varchar(1)
	dosage_unit					varchar(40)
	notes						varchar(2000)
    ingredient_f                varchar(160)*
    strength_unit_f             varchar(80)*
    strength_type_f             varchar(80)*
    dosage_unit_f               varchar(80)*
"""

"""
COMPANIES
	drug_code					int(8)
	mfr_code					varchar(5)
	company_code				int(6)
	company_name				varchar(90)
	company_type				varchar(40)
	address_mailing_flag		varchar(1)
	address_billing_flag		varchar(1)
	address_notification_flag	varchar(1)
	address_other				varchar(1)
	suite_number				varchar(20)
	street_name					varchar(80)
	city_name					varchar(60)
	province					varchar(40)
	country						varchar(40)
	postal_code					varchar(20)
	post_office_box				varchar(15)
    province_f                  varchar(40)*
    country_f                   varchar(40)*
"""
"""
DRUG_PRODUCT
	drug_code					int(8)
	product_categorization		varchar(80)
	class						varchar(40)
	drug_identification_number	varchar(8)
	brand_name					varchar(200)	
	descriptor					descriptor(210)
	pediatric_flag				varchar(1)
	accession_number			varchar(5)
	number_of_ais				varchar(10)
	last_update_date			date
	ai_group_no					varchar(10)
    class_f                     varchar(40)*
    brand_name_f                varchar(200)*
    descriptor_f                varchar(150)*
"""
"""
STATUS
	drug_code					int(8)
	current_status_flag			varchar(1)
	status						varchar(40)
	history_date				date
    status_f                    varchar(80)*
    lot_number                  varchar(80)*
    expiration_date             date*
"""
"""
FORM
	drug_code					int(8)
	pharm_form_code				int(7)
	pharmaceutical_form			varchar(40)
    pharmaceutical_form_f       varchar(40)*
"""
"""
PACKAGING
	drug_code					int(8)
	upc							varchar(12)
	package_size_unit			varchar(40)
	package_type				varchar(40)
	package_size_unit			varchar(10)
	product_information			varchar(90)
    package_size_unit_f         varchar(80)*
    package_type_f              varchar(80)*
"""
"""
PHARMACEUTICAL_STD
	drug_code					int(8)
	pharmaceutical_std			varchar(40)
"""
"""
ROUTE
	drug_code					int(8)
	route_of_administration_code int(6)
	route_of_administration		varchar(40)
    route_of_administration_f   varchar(40)*
"""
"""
SCHEDULE
	drug_code					int(8)
	schedule					varchar(40)
    schedule_f					varchar(40)*
"""
"""
THERAPEUTIC_CLASS
	drug_code					int(8)
	tc_atc_number				varchar(8)
	tc_atc						varchar(120)
	tc_ahfs_number				varchar(20)
	tc_ahfs						varchar(80)
    tc_atc_f                    varchar(120)*
    tc_ahfs_f                   varchar(80)*
"""
"""
VETERINARY_SPECIES
	drug_code					int(8)
	vet_species					varchar(80)
	vet_sub_species				varchar(80)
    vet_species_f               varchar(80)*
"""