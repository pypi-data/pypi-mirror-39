from cgrates.client.apier_v1 import ClientV1
from cgrates.client.apier_v2 import ClientV2


class Client(ClientV1, ClientV2):

    def __init__(self, tenant):
        self.tenant = tenant
