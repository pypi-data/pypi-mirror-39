from cgrates import models
from cgrates.client.base import BaseClient


class ClientV2(BaseClient):

    def get_accounts(self):

        method = "ApierV2.GetAccounts"

        params = {
            "Tenant": self.tenant,
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return [models.Account.from_result(x) for x in data]

    def get_account(self, account: str):

        method = "ApierV2.GetAccount"

        params = {
            "Tenant": self.tenant,
            "Account": account
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        return models.Account.from_result(data)

    def add_account(self, account: str, action_plan_id: str ="", action_trigger_id: str="", allow_negative=False):

        method = "ApierV2.SetAccount"

        params = {
            "tenant": self.tenant,
            "Account": account,
            "ActionPlanID": action_plan_id,
            "ActionPlansOverwrite": True,
            "ActionTriggerID": action_trigger_id,
            "ActionTriggerOverwrite": True,
            "AllowNegative": allow_negative,
            "Disabled": False,
            "ReloadScheduler": True
        }

        data, error = self.call_api(method, params=[params])

        if error:
            raise Exception("{} returned error: {}".format(method, error))

        if data != "OK":
            raise Exception("{} returned {}".format(method, data))

        return self.get_account(account)
