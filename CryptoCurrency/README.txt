UsChat_v2
------------------

1. Install wxpy.
    Based on itchat, wxpy improves module usability and enriches functionality through a large number of interface optimizations.
    The command to install wxpy:
    pip3 install -U wxpy

2. create subdir "data"; put all the training data *.yml to the subdir 'data'.

3. Run python3 UsChat_v2.py in the main dir; follow the procedure to scan the 2-dimenional code to login into your wechat.

   Notes: You have to modify the file UsChat_v2.py to use your group name in your account. Just replace the name '东山之家' with the group name you are interested in setting auto reply.

CryptoCurrencyChat
------------------
(All commands below have been tested on Linux enviroment on MacBook Pro 2015)

1. chatterbot
    ChatterBot is a Python library that makes it easy to generate automated responses to a user’s input. ChatterBot uses a selection of machine learning algorithms to produce different types of responses. This makes it easy for developers to create chat bots and automate conversations with users.
    For more details: 
        http://chatterbot.readthedocs.io/en/stable/index.html
    To install ChatterBot from PyPi using pip run the following command in your terminal.
    Command: pip3 install chatterbot 
    Note: install python3 and pip3 if not done yet.

2. Collect the data for cryptocurrency. 
   Source code: 
     GetQuestions.py - used to get question links under one key word. In my case, I chose "cryptocurrency" and "bitcoin".Those questions links will be stored in crypto_questions.txt
     GetAnswers.py - used to get question titles and answers form quora. It will visit each link form crypto_questions.txt, and then get the titles and answers. All tiles and answers are saved in the file quora.yml.

   data format (.yml) (for data training purpose, the question begins with "- - ", and in the next line the answer which begins with "  - " follows. See example file cryptocurrency.yml):
       categories:
       - cryptocurrency
       conversations:
       - - Price of Bitcoin
         - Current price of bit is $8,000.12
       - - what is cryptocurrecny
         - Cryptocurrency is a medium of exchange, created and stored electronically in the blockchain

3. Train data.
    ChatterBot comes with a corpus data and utility module that makes it easy to quickly train your bot to communicate. To do so, simply specify the corpus data modules and/or file paths you want to use.

**********************************************
chatterbot = ChatBot("Training Example")
chatterbot.set_trainer(ChatterBotCorpusTrainer)

chatterbot.train(
    "chatterbot.corpus.english"
)

chatterbot.train(
    "./data/greetings_corpus/custom.corpus.json",
    "./data/my_corpus/"
)
**********************************************


4. Logic Adapter for calling cryptocurrency price quote API.
    Source code: cryptocurrency_logic.py
    Assuming that you have a class named CryptocurrencyLogicAdapter in your cryptocurrency_logic.py file, you should be able to specify the following when you initialize your chat bot.

**********************************************
ChatBot(
    # ...
    logic_adapters=[
        {
            'import_path': 'cool_chatbot.MyLogicAdapter'
        }
    ]
)
**********************************************

    API endpoint used for getting cryptocurrency price quote:
        https://api.coinmarketcap.com/v1/ticker/bitcoin/
 
5. itchat & chatterbot:
    Installing itchat: pip3 install wechat
    A complete and graceful API for Wechat interface. Automatically respond to your own text message. YOu need to set up wechat account.
    For more details:
        http://itchat.readthedocs.io/zh/latest/

**********************************************
import itchat

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    return msg.text

itchat.auto_login()
itchat.run()
**********************************************

6. The script to automatically send the response for the incoming question to your wechat account. Implement itchat API call inside chatterbot, using sqlite3 db to save the data:
    Source code: UsChat.py

    a. Create the class CryptoCurrency for question and answer;
    b. Set up sqlite3 file based database;
    c. Initiate chatterbot with the correct settings;
    d. Create the method to call chatterbot API to get the response of the wechat message via itchat API interface, and save the question and response in db.
    e. Let itchat run after auto_login

# reply to the user when question is asked
# wechat robot application
# need to scan your two-dimension code for wechat authentication

7. Django (optional)
    Django is a free and open-source web framework, written in Python. ChatterBot has direct support for integration with Django. ChatterBot provides out of the box models and endpoints that allow you build ChatterBot powered Django applications. To run chatterbot on web server, you may use Django app.
    Command: pip3 install Django

    For the training data usage on django app, 
    Command: python3 manage.py train (under mysite directory)
------------------------------------------------------------
Notes:
a). For cryptocurrency API:

https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD
https://api.coinmarketcap.com/v1/ticker/
https://api.coinmarketcap.com/v1/ticker/bitcoin/

b). Tope 20 cryptocurrencies:

**********************************************
# get top 20 cryptocurrency prices
response = requests.get("https://api.coinmarketcap.com/v1/ticker/?limit=20")

priceInfo = json.loads(response.text)
for price in priceInfo:
    print(price['id'], price['symbol'], price['price_usd'])
**********************************************

bitcoin BTC 9339.93
ethereum ETH 683.734
ripple XRP 0.869365
bitcoin-cash BCH 1427.52
eos EOS 21.4928
cardano ADA 0.37285
litecoin LTC 152.63
stellar XLM 0.447563
neo NEO 88.0919
tron TRX 0.0865156
iota MIOTA 2.04471
monero XMR 251.539
dash DASH 490.67
nem XEM 0.419282
vechain VEN 4.72317
tether USDT 0.995183
ethereum-classic ETC 21.5793
qtum QTUM 22.5594
omisego OMG 17.865
icon ICX 4.65955
binance-coin BNB 14.8695
bitcoin-gold BTG 76.7963
lisk LSK 12.3323
aeternity AE 5.10941
zcash ZEC 298.236

------------------------------------------------------------
If there is any question on this doc, please email me qxie1@umbc.edu. Thank you!
