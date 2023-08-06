import datetime
import pprint
import requests
import yaml
from yahoo_finance_api2.exceptions import YahooFinanceError

PERIOD_TYPE_DAY = 'day'
FREQUENCY_TYPE_MINUTE = 'm'

class Share(object):

    def __init__(self, symbol):
        self.symbol = symbol


    def get_historical(self, period_type, period, frequency_type, frequency):
        data = self._download_symbol_data(period_type, period, 
                                         frequency_type, frequency)

        # for i in range(len(data['timestamp'])):
        #     if i < (len(data['timestamp']) - 1):
        #         print(datetime.datetime.utcfromtimestamp(
        #                 data['timestamp'][i + 1]
        #             ).strftime('%Y-%m-%d %H:%M:%S'), 
        #             data['timestamp'][i + 1] - data['timestamp'][i]
        #         )

        if 'timestamp' not in data:
            return None

        return_data = {
            'timestamp': data['timestamp'],
            'open': data['indicators']['quote'][0]['open'],
            'high': data['indicators']['quote'][0]['high'],
            'low': data['indicators']['quote'][0]['low'],
            'close': data['indicators']['quote'][0]['close'],
            'volume': data['indicators']['quote'][0]['volume']
        }

        return return_data    
    
    def _set_time_frame(self, periodType, period):
        now = datetime.datetime.now()
        if periodType == PERIOD_TYPE_DAY:
            period = min(period, 59)
            start_time = now - datetime.timedelta(days=period)
        end_time = now

        return start_time.strftime("%s"), end_time.strftime("%s")


    def _download_symbol_data(self, period_type, period, 
                              frequency_type, frequency):
        start_time, end_time = self._set_time_frame(period_type, period)
        url = (
            'https://query1.finance.yahoo.com/v8/finance/chart/{0}?symbol={0}'
            '&period1={1}&period2={2}&interval={3}&'
            'includePrePost=true&events=div%7Csplit%7Cearn&lang=en-US&'
            'region=US&crumb=t5QZMhgytYZ&corsDomain=finance.yahoo.com'
        ).format(self.symbol, start_time, end_time, 
                 self._get_frequency_str(frequency_type, frequency))

        resp_json = requests.get(url).json()

        if self._is_yf_response_error(resp_json):
            self._raise_yf_response_error(resp_json)
            return

        data_json = resp_json['chart']['result'][0]

        return data_json


    def _is_yf_response_error(self, resp):
        return resp['chart']['error'] is not None


    def _raise_yf_response_error(self, resp):
        raise YahooFinanceError(
            '{0}: {1}'.format(
                resp['chart']['error']['code'],
                resp['chart']['error']['description']
            )
        )

    def _get_frequency_str(self, frequency_type, frequency):
        return '{1}{0}'.format(frequency_type, frequency)
