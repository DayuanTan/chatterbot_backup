from chatterbot.logic import LogicAdapter
import requests
from chatterbot.conversation import Statement


class CryptocurrencyLogicAdapter(LogicAdapter):
    def __init__(self, **kwargs):
        super(CryptocurrencyLogicAdapter, self).__init__(**kwargs)

    def can_process(self, statement):
        """
        Return true if the input statement contains
        'price' and one of top rank 25 cryptocurrencies.
        """

        if 'price' not in statement.text.lower().split():
            return False

        words = ['bitcoin', 'ethereum', 'ripple', 'bitcoin-cash', 'eos',
            'cardano', 'litecoin', 'stellar', 'neo', 'tron', 'iota', 'monero',
            'dash', 'nem', 'vechain', 'tether', 'ethereum-classic',
            'qtum', 'omisego', 'icon', 'binance-coin', 'bitcoin-gold',
            'lisk', 'aeternity', 'zcash']

        for x in words:
            if x in statement.text.lower().split():
               return True

        return False

    def process(self, statement):

        words = ['bitcoin', 'ethereum', 'ripple', 'bitcoin-cash', 'eos',
            'cardano', 'litecoin', 'stellar', 'neo', 'tron', 'iota', 'monero',
            'dash', 'nem', 'vechain', 'tether', 'ethereum-classic',
            'qtum', 'omisego', 'icon', 'binance-coin', 'bitcoin-gold',
            'lisk', 'aeternity', 'zcash']

        currency = ''
        for x in words:
            if x in statement.text.lower().split():
                currency = x 
                break

        url = "https://api.coinmarketcap.com/v1/ticker/"

        # Make a request to the coinmarketcap API
        response = requests.get(url + currency + "/")

        data = Statement('The current price of ' + currency +
            ' is $' + response.json()[0]['price_usd'])

        # Let's base the confidence value on if the request was successful
        if response.status_code == 200:
            confidence = 1
        else:
            confidence = 0

        data.confidence = confidence

        return data
