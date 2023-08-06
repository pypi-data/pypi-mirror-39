import hashlib
import hmac
import base64
from dotenv import load_dotenv, find_dotenv
import requests
from datetime import datetime
import os
import jwt


dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

general_api = 'https://jsapi.settle.finance/api'
price_api = 'https://dbapi.settle.finance/api'
chat_api = 'https://chat.settle.finance/v1/api'

# Auth Deployed in Production
issuer = "99990979-7c8c-4511-9f83-fdd3d0dd91e3";
authority_URL = "https://auth.settle.finance";

audience_prod = "ffffd16f-28c1-49d6-8fc2-010b972d2dcf";
audience_all = "*";

certyficate = "-----BEGIN PUBLIC KEY-----\nMIICIjANBgkqhkiG9w0BAQEFAAOCAg8AMIICCgKCAgEAijHFBjjZDOJ1Eixed7h6\n+12nKnOPq7zYsMI05YHidUCwcfgOCmJOgeZ/NCo8QVcA9rqVS4uf0eLrm3zEuP9w\nn/zFLrxwsV4498KqS1wNha3yEnuBGQeCwT1zjdlSaqRWxzxkt321B1rLK0eyPfTi\n2oJunNPgVu68R40QavaWqt8JCNd6fhgtI0mHnIi4Xh4pri6TGdzofjNtjvCCttUw\nc2yHW9bWJ3m32lPLIRJYzylmtp6HXEkODlxaHQEjr4ff8ZxMk0VJgzBHiYzy3Wtm\ncwEMeCibwsrpaFzwSA5zcnxwpAYtxvw9fdCb8mCVpZjwAXjjKYa/bND8YfxYqTHu\ny8d/EvJOg9OWeqGdrZ9IBUhm+O3UdA0XQX4rTQg0UHqm09sqLSAy6kP6oEc8b498\nwvRZEc3BfaEBQWYhD9cREnzxLSnVUK3o/5ey6hH7ZPSnhPS405qpFkZqe8mOAXpY\n0cHfjWuLjqlstZBnF860fGHTT2vPHEuQ+A8XJ2dF2Az60rLri4WWTAjdQ7HATKZm\nGH0YSnhx2xqvm+XCG1M1ykzAmj0eeyF7Ms1vmVMjmTWfvmNLQ4kA0Ar0U9Ks9FP+\nYEmeuWK4IeCfQhrpf0mqCRzTdb9/AQvRklyq8hn1XZsaB9Et45WCb+v5WIiaUN/O\nNtKnbUl3IM5xuIKXeI6f+okCAwEAAQ==\n-----END PUBLIC KEY-----";

class _SettleBase:
    def __init__(self, api, api_key=None, api_secret=None):
        self.__api_key = os.getenv("SETTLE_API_KEY") if api_key is None else api_key
        self.__api_secret = os.getenv("SETTLE_API_SECRET") if api_secret is None else api_secret
        self.__access_key = None
        self.__signature = None
        self.__api = api if os.getenv("ENVIRONMENT") != 'development' else 'https://localhost:3005'

    def __generate_url(self, endpoint):
        if endpoint[0] != '/':
            endpoint = "{}/{}".format(self.__api, endpoint)
        else:
            endpoint = "{}{}".format(self.__api, endpoint)

        return endpoint

    def __get_access_key(self):
        r = requests.get(
            self.__generate_url('app/AccessToken'),
             headers={'X-Api-Key': self.__api_key}
        )

        self.__access_key_time = datetime.now()
        self.__access_key = r.json()['accessToken']

        return self.__access_key

    def __get_signature(self):
        return base64.b64encode(
            hmac.new(
                bytes(self.__api_secret.encode('utf-8')),
                bytes(self.__access_key.encode('utf-8')),
                digestmod=hashlib.sha256).digest()).decode()

    def __get_request_header(self):
            return {
                'X-Api-Key': self.__api_key,
                'X-Access-Token': self.__get_access_key(),
                'X-Api-Signature': self.__get_signature()
            }

    def __generate_request(self, endpoint, params={}):
        return requests.get(
            self.__generate_url(endpoint),
            params=params,
            headers=self.__get_request_header()
        )



class PriceList(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, price_api)

    def price_history(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/price-history', params)
        data = r.json()
        return data if not include_response else (data, r)


    def info(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/info', params)
        data = r.json()
        return data if not include_response else (data, r)

    def ticker(self, params={}, include_response=False):
        r = super(PriceList, self)._SettleBase__generate_request('/public/ticker', params)
        data = r.json()
        return data if not include_response else (data, r)


class Portfolio(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)

    def summary(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Summary', params)
        data = r.json()
        return data if not include_response else (data, r)

    def holdings(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Holdings', params)
        data = r.json()
        return data if not include_response else (data, r)

    def holdings_with_trades(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/HoldingsWithTrades', params)
        data = r.json()
        return data if not include_response else (data, r)

    def trades(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Trades', params)
        data = r.json()
        return data if not include_response else (data, r)

    def exchanges(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/Exchanges', params)
        data = r.json()
        return data if not include_response else (data, r)

    def balance_history(self, params={}, include_response=False):
        r = super(Portfolio, self)._SettleBase__generate_request('/public/PortfolioTracker/BalanceHistory', params)
        data = r.json()
        return data if not include_response else (data, r)


class Users(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)
        pass

    def guid_to_username(self, params={}, include_response=False):
        r = super(Users, self)._SettleBase__generate_request('/app/GuidToUsername', params)
        data = r.content.decode('utf-8')
        return data if not include_response else (data, r)

    def exchange_token_for_guid(self, params={}, include_response=False):
        data = jwt.decode(params['token'], certyficate, audience=audience_all)
        r = None
        return data['nameid'] if not include_response else (data, r)


class Chat(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, chat_api)
        pass

    def send_event(self, params={}, include_response=False):
        r = super(Chat, self)._SettleBase__generate_request('/app/event', params)
        data = r.content.decode('utf-8')
        return data if not include_response else (data, r)


class App(_SettleBase):
    def __init__(self):
        _SettleBase.__init__(self, general_api)

    def users(self, params={}, include_response=False):
        r = super(App, self)._SettleBase__generate_request('/app/Users', params)
        data = r.json()
        return data if not include_response else (data, r)

    def send_notification(self, params={}, include_response=False):
        r = super(App, self)._SettleBase__generate_request('/app/SendNotification', params)
        data = r.content.decode('utf-8')
        return data if not include_response else (data, r)


