from django.db import models

"""
    Planning for expanding the drug price calculator
    
    List of medications
    Trade name
    Brand Name
    Ingredients +/- strengths +/- dosage form (EPID?)
    ptcFK
    atcFK

    Price info
        medicationFK
        unit price
        unit of issue
        LCA
        MAC
        source
            ABC iDBL
            ABC DPL
            NIHB

    PTC List
        
    ATC List

    Coverage
        ABC coverage
            Plan coverage amounts
            ABC special auth
        NIHB coverage
            Prior approval
"""
# Create your models here.

"""abc_atc table
id          AI      PK
url         int(10)
atc_1       varchar(7)
act_1_text  varchar(200)
atc_2       varchar(7)
act_2_text  varchar(200)
atc_3       varchar(7)
act_3_text  varchar(200)
atc_4       varchar(7)
act_4_text  varchar(200)
atc_5       varchar(7)
act_5_text  varchar(200)
"""

"""abc_coverage table
id              AI     PK
url             int(10)
coverage        varchar(50)
criteria        tinyint(1)
criteria_sa     varchaer(100)
criteria_p      varchar(70)
group_1         tinyint(1)
group_66        tinyint(1)
group_66a       tinyint(1)
group_19823     tinyint(1)
group_19823a    tinyint(1)
group_19824     tinyint(1)
group_20400     tinyint(1)
group_20403     tinyint(1)
group_20514     tinyint(1)
group_22128     tinyint(1)
group_23609     tinyint(1)
"""

"""abc_extra_information table
id                  AI      PK
url                 int(10)
date_listed         date
date_discontinued   date
manufacturer        varchar(50)
schedule            varchar(10)
interchangeable     varchar(3)
"""

"""abc_price table
id              AI      PK
url             int(10)
din             int(8)
brand_name      varchar(70)
strength        varchar(200)
route           varchar(20)
dosage_form     varchar(35)
generic_name    varchar(450)
unit_price      decimal(10,4)
lca             decimal(10,4)
lca_text        varchar(150)
unit_issue      varchar(25)
"""

"""abc_ptc table
id          AI      PK
url         int(10)
ptc_1       int(8)
ptc_1_text  varchar(75)
ptc_2       int(8)
ptc_2_text  varchar(75)
ptc_3       int(8)
ptc_3_text  varchar(75)
ptc_4       int(8)
ptc_4_text  varchar(75)
"""

"""abc_special_authorization table
id      int(11)
url     int(10)
title   varchar(200)
link    varchar(50)
"""