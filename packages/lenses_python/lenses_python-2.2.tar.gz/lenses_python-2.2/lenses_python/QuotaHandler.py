from requests import get, delete, post, put
import json
from lenses_python.constants import QUOTAS_END_POINT, QUOTAS__USERS_END_POINT, QUOTAS_CLIENTS_END_POINT

class QuotaHandler:

    def __init__(self, token, url):
        self.token = token
        self.url = url
        self.quotas_end_point = QUOTAS_END_POINT
        self.quotas_users_end_point = QUOTAS__USERS_END_POINT
        self.quotas_clients_end_point = QUOTAS_CLIENTS_END_POINT
        self.default_headers = {'Content-Type': 'application/json', 'Accept': 'application/json',
                                'x-kafka-lenses-token': self.token}

    def GetQuotas(self):
        """
        Get Quotas
        :return:
        """
        url = self.url+self.quotas_end_point
        response = get(url, headers=self.default_headers)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))
        return response.json()

    def SetQuotasAllUsers(self, config):
        """
         Create/Update Quota - All Users
        :param config:{
                         "producer_byte_rate" : "100000",
                         "consumer_byte_rate" : "200000",
                         "request_percentage" : "75"
                      }
        :return:
        """
        url = self.url+self.quotas_users_end_point
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def SetQuotaUserAllClients(self, user, config):
        """
        Create/Update Quota - User all Clients
        Create/update for all client ids for a user.

        :param user:The user to set the quota for
        :param config:{
                       "producer_byte_rate" : "100000",
                       "consumer_byte_rate" : "200000",
                       "request_percentage" : "75"
                       }
                       The quota contrain
        :return:
        """
        url_extend = self.quotas_users_end_point+"/"+user+"/clients"
        url = self.url + url_extend
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def SetQuotaUserClient(self, user, clientid, config):
        """
         Quotas for a user and client id pair.


        :param user:The user to set the quota for
        :param clientid:The client id to set the quota for
        :param config:The quota contraints
                     {
                      "producer_byte_rate" : "100000",
                      "consumer_byte_rate" : "200000",
                      "request_percentage" : "75"
                     }
        :return:
        """
        url_extend = self.quotas_users_end_point+"/"+user+"/clients/"+clientid
        url = self.url+url_extend
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def SetQuotaUser(self, user, config):
        """
        Quota for a user.

        :param user:The user to set the quota for
        :param config: The quota contraints
                       {
                        "producer_byte_rate" : "100000",
                        "consumer_byte_rate" : "200000",
                        "request_percentage" : "75"
                       }
        :return:
        """
        url_extend = self.quotas_users_end_point+"/"+user
        url = self.url+url_extend
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def SetQuotaAllClient(self, config):
        """
        Default for all clients.

        :param config:The quota contraints,
                       {
                        "producer_byte_rate" : "100000",
                        "consumer_byte_rate" : "200000",
                        "request_percentage" : "75"
                      }
        :return:
        """
        url = self.url+self.quotas_clients_end_point
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def SetQuotaClient(self, clientid, config):
        """
        Quotas for a client id.

        :param clientid:The client id to set the quota for
        :param config: The quota contraints,
                       {
                        "producer_byte_rate" : "100000",
                        "consumer_byte_rate" : "200000",
                        "request_percentage" : "75"
                       }
        :return:
        """
        url_extend = self.quotas_clients_end_point+"/"+clientid
        url = self.url+url_extend
        response = put(url, headers=self.default_headers, json=config)
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQutaAllUsers(self, config):
        """
        Delete default for all users.
        :param config: A list we the parameters which want to delete
        :return:
        """
        url = self.url+self.quotas_users_end_point
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQuotaUserAllClients(self, user, config):
        """
        Delete for all client ids for a user.


        :param user:
        :param config: A list we the parameters which want to delete
        :return:
        """
        url_extend = self.quotas_users_end_point+user+"/clients"
        url = self.url+url_extend
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQuotaUserClient(self, user, clientid, config):
        """
        Delete a Quota - User/Client pair
        :param user:The user to set the quota for
        :param clientid:The client id to set the quota for
        :param config: A list we the parameters which want to delete
        :return:
        """
        url_extend = self.quotas_users_end_point+"/"+user+"/clients/"+clientid
        url = self.url+url_extend
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQuotaUser(self, user, config):
        """
        Delete a quota for a user.
        :param user:The user to set the quota for
        :param config: A list we the parameters which want to delete
        :return:
        """
        # url_extend = "/api/quotas/users/"+user
        url_extend = self.quotas_users_end_point+"/"+user
        url = self.url+url_extend
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQuotaAllClients(self, config):
        """
        Delete defaults for all clients.
        :param config: A list we the parameters which want to delete
        :return:
        """
        url = self.url+self.quotas_clients_end_point
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))

    def DeleteQuotaClient(self, clientid, config):
        """
        Delete a Quota - Client
        Delete a quotas for a client id.

        :param clientid: The client id to set the quota for
        :param config: A list we the parameters which want to delete
        :return:
        """
        url_extand = self.quotas_clients_end_point+"/"+clientid
        url = self.url+url_extand
        response = delete(url, headers=self.default_headers, data=json.dumps(config))
        if response.status_code != 200:
            raise Exception("Http status code {}.{}".format(response.status_code, response.text))
