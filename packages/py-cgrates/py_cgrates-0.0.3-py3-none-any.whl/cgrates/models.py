import json
from cgrates import schema


class BaseModel:
    def to_dict(self):
        return self.SCHEMA().dump(self)


class Destination(BaseModel):
    SCHEMA = schema.DestinationSchema

    def __init__(self, destination_id, prefixes):
        self.destination_id = destination_id
        self.prefixes = prefixes

    @classmethod
    def from_result(self, result):
        data = {
            'destination_id': result["Id"],
            'prefixes': result["Prefixes"]
        }

        return self(**data)

    def __repr__(self):
        return '<Destination({}, [{}])>'.format(self.destination_id, ",".join(self.prefixes))


class Account(BaseModel):
    SCHEMA = schema.AccountSchema

    def __init__(self, account: str, allow_negative: bool = False, disabled: bool = False):
        self.account = account
        self.allow_negative = allow_negative
        self.disabled = disabled

    def __repr__(self):
        return '<Account({})>'.format(self.account)

    @classmethod
    def from_result(self, result):

        data = {
            'account': result['ID'].split(":")[1],
            'allow_negative': result["AllowNegative"],
            'disabled': result["Disabled"],
        }

        return self(**data)


class Rate(BaseModel):
    SCHEMA = schema.RateSchema

    def __init__(self, rate: float, rate_unit: int, rate_increment: int, group_interval_start: int = 0,
                 connect_fee: int = 0):
        self.rate = rate
        self.rate_unit = rate_unit
        self.rate_increment = rate_increment
        self.group_interval_start = group_interval_start
        self.connect_fee = connect_fee

    def __repr__(self):
        return '<Rate(rate={self.rate}, rate_unit={self.rate_unit},...)>'.format(self=self)

    @classmethod
    def from_result(self, result):
        data = {
            'rate': result["Rate"],
            'rate_unit': result["RateUnit"],
            'rate_increment': result["RateIncrement"],
            'group_interval_start': result["GroupIntervalStart"],
            'connect_fee': result["ConnectFee"],
        }

        return self(**data)


class DestinationRate(BaseModel):
    SCHEMA = schema.DestinationRateSchema

    def __init__(self, rate_id: str, dest_id: str, rounding_method: str = "*up", rounding_decimals: int = 4,
                 max_cost: float = 0, max_cost_strategy: str = ""):
        self.rate_id = rate_id
        self.dest_id = dest_id
        self.rounding_method = rounding_method
        self.rounding_decimals = rounding_decimals
        self.max_cost = max_cost
        self.max_cost_strategy = max_cost_strategy

    def __repr__(self):
        return '<DestinationRate(rate_id={self.rate_id}, dest_id={self.dest_id},...)>'.format(self=self)

    @classmethod
    def from_result(self, result):
        data = {
            'rate_id': result["RateId"],
            'dest_id': result["DestinationId"],
            'rounding_method': result["RoundingMethod"],
            'rounding_decimals': result["RoundingDecimals"],
            'max_cost': result["MaxCost"],
            'max_cost_strategy': result["MaxCostStrategy"],
        }

        return self(**data)


class RatingPlan(BaseModel):
    SCHEMA = schema.RatingPlanSchema

    def __init__(self, dest_rate_id: str, timing_id: str, weight: int = 10):
        self.DestinationRatesId = dest_rate_id
        self.TimingId = timing_id
        self.Weight = weight

    def __repr__(self):
        return '<RatingPlan(dest_rate_id={self.DestinationRatesId}, timing_id={self.TimingId},...)>'.format(self=self)
