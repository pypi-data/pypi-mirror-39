# Python CGRateS Api Client

WIP

See: https://github.com/cgrates/cgrates



## Install

    pip install py-cgrates

## Usage

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
    
