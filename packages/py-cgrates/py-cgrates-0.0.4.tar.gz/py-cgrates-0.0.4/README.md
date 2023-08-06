# Python CGRateS Api Client

WIP

See: https://github.com/cgrates/cgrates



## Install

    pip install py_cgrates

## Usage 

## Account Management - Create

    from cgrates import Client
    from cgrates import models
    
    api = Client(tenant="1")
    
    api.add_account(name="AcmeWidgets")
    
    => <Account(AcmeWidgets)>
    
    api.add_destination("DST_45", prefixes=["45"])
    
    => <Destination(DST_64, [64])>
    
    api.add_rates(rate_id="RT_STANDARD", rates=[models.Rate(rate=0.25, rate_unit=60, rate_increment=60)])
    
    => [<Rate(rate=0.25, rate_unit=60s,...)>]
    
    api.add_destination_rates(dest_rate_id="DR_64", 
            dest_rates=[models.DestinationRate(rate_id="RT_STANDARD", dest_id="DST_64")])

    => [<DestinationRate(rate_id=RT_STANDARD, dest_id=DST_64,...)>]
    
    api.add_rating_plan(rating_plan_id="RP_XX", 
            rating_plans=[models.RatingPlan(dest_rate_id="DR_65_65", timing_id="ALWAYS")])
    
    => [<RatingPlan(dest_rate_id=DR_65_65, timing_id=ALWAYS,...)>]


## Account Management - Get/List
    
    api.get_accounts()
    
    => [<Account(AcmeWidgets)>]
    
    api.get_account(account="AcmeWidgets")
    
    => <Account(AcmeWidgets)>
    
    api.get_destination(destination_id="DST_64")
    
    => <Destination(DST_64, [64])>
    
    api.get_rates(rate_id="RT_STANDARD")
    
    [<Rate(rate=0.25, rate_unit=60s,...)>]
    
    api.get_rating_plan(rating_plan_id="RP_XX")
    
    =>  [<RatingPlan(dest_rate_id=DR_65_65, timing_id=ALWAYS,...)>]


    
    