from typing import List
from cgrates import models
from cgrates.client.base import BaseClient


class ClientV1(BaseClient):

    def get_destination(self, destination_id: str):

        self.ensure_valid_tag(name="destination_id", value=destination_id, prefix="DST")

        method = "ApierV1.GetDestination"

        data, error = self.call_api(method, params=[destination_id])

        if error:
            if error == "NOT_FOUND":
                return None
            else:
                raise Exception("{} returned error: {}".format(method, error))

        return models.Destination.from_result(data)

    def add_destination(self, destination_id: str, prefixes):

        self.ensure_valid_tag(name="destination_id", value=destination_id, prefix="DST")

        method = "ApierV1.SetTPDestination"

        params = {
            "id": destination_id,
            "Prefixes": prefixes,
            "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        # Refresh data_db
        method = "ApierV1.LoadDestination"

        params = {
            "id": destination_id,
            "TPid": self.tenant,
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return self.get_destination(destination_id=destination_id)

    def get_rates(self, rate_id: str):

        self.ensure_valid_tag(name="rate_id", value=rate_id, prefix="RT")

        method = "ApierV1.GetTPRate"

        params = {
            "Id": rate_id,
            "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            if error == "NOT_FOUND":
                return None
            else:
                raise Exception("{} returned error: {}".format(method, error))

        return [models.Rate.from_result(r) for r in data['RateSlots']]

    def add_rates(self, rate_id: str, rates: List[models.Rate]):

        self.ensure_valid_tag(name="rate_id", value=rate_id, prefix="RT")

        method = "ApierV1.SetTPRate"

        params = {
            "Id": rate_id,
            "RateSlots": [r.to_dict() for r in rates],
            "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return self.get_rates(rate_id=rate_id)


    def get_destination_rates(self, dest_rate_id: str):

        self.ensure_valid_tag(name="dest_rate_id", value=dest_rate_id, prefix="DR")

        method = "ApierV1.GetTPDestinationRate"

        params = {
            "TPid": self.tenant,
            "ID": dest_rate_id
        }

        data, error = self.call_api(method, params=[params])

        if error:
            if error == "NOT_FOUND":
                return None
            else:
                raise Exception("{} returned error: {}".format(method, error))

        return [models.DestinationRate.from_result(dr) for dr in data['DestinationRates']]

    def add_destination_rates(self, dest_rate_id: str, dest_rates: List[models.DestinationRate]):

        self.ensure_valid_tag(name="dest_rate_id", value=dest_rate_id, prefix="DR")

        # todo: confirm rates and destinations first?

        method = "ApierV1.SetTPDestinationRate"

        params = {
            "Id": dest_rate_id,
            "DestinationRates": [dr.to_dict() for dr in dest_rates],
            "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        if data != "OK":
            raise Exception("{} returned {}".format(method, data))

        return self.get_destination_rates(dest_rate_id=dest_rate_id)

    def get_rating_plan(self, rating_plan_id: str):

        self.ensure_valid_tag(name="rating_plan_id", value=rating_plan_id, prefix="RP")

        method = "ApierV1.GetTPRatingPlan"

        params = {
                    "Id": rating_plan_id,
                    "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return [models.RatingPlan.from_result(rp) for rp in data['RatingPlanBindings']]


    def add_rating_plan(self, rating_plan_id: str, rating_plans: List[models.RatingPlan]):

        self.ensure_valid_tag(name="rating_plan_id", value=rating_plan_id, prefix="RP")

        # todo: confirm rating_plans are valid

        method = "ApierV1.SetTPRatingPlan"

        params = {
            "Id": rating_plan_id,
            "RatingPlanBindings": [rp.to_dict() for rp in rating_plans],
            "TPid": self.tenant
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return self.get_rating_plan(rating_plan_id=rating_plan_id)
