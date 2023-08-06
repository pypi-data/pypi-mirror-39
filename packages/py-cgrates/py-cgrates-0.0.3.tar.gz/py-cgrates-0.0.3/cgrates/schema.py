from marshmallow import Schema, fields


class Seconds(fields.Int):

    def _serialize(self, value, attr, obj, **kwargs):
        value = super(Seconds, self)._serialize(value, attr, obj, *kwargs)
        return "{}s".format(value)


class AccountSchema(Schema):
    Account = fields.Str(attribute="account")
    AllowNegative = fields.Boolean(required=True, attribute="allow_negative")
    Disabled = fields.Boolean(default=False, attribute="disabled")


class DestinationSchema(Schema):
    Id = fields.Str(required=True, attribute="destination_id")
    Prefixes = fields.List(fields.Str(), attribute="prefixes")


class RateSchema(Schema):
    ConnectFee = fields.Float(default=0, attribute="connect_fee")
    Rate = fields.Float(required=True, attribute="rate")
    RateUnit = Seconds(required=True, attribute="rate_unit")
    RateIncrement = Seconds(required=True, attribute="rate_increment")
    GroupIntervalStart = Seconds(required=True, attribute="group_interval_start")


class DestinationRateSchema(Schema):
    RateId = fields.Str(required=True, attribute="rate_id")
    DestinationId = fields.Str(required=True, attribute="dest_id")
    RoundingMethod = fields.Str(attribute="rounding_method")
    RoundingDecimals = fields.Int(attribute="rounding_decimals")
    MaxCost = fields.Float(attribute="max_cost")
    MaxCostStrategy = fields.Str(attribute="max_cost_strategy")


class RatingPlanSchema(Schema):
    DestinationRatesId = fields.Str(required=True)
    TimingId = fields.Str(required=True)
    Weight = fields.Int()
