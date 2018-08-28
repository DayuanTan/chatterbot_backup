
from chatterbot import ChatBot
from chatterbot.utils import get_response_time
import itchat

from sqlalchemy import Column, Integer, String, Sequence
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:///cyptocurrency.db', echo=True)
Base = declarative_base()

class CryptoCurrency(Base):
    __tablename__ = 'crypto_currency'

    id = Column(Integer, primary_key=True)
    question = Column(String)
    answer = Column(String)

    def __repr__(self):
       return "<CryptoCurrency(question='%s', answer='%s')>" % (
                            self.question, self.answer)

# sqllite3 database connection
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

chatbot = ChatBot(
    'Export Example Bot',
    trainer='chatterbot.trainers.ChatterBotCorpusTrainer',
    logic_adapters=[
        {'import_path': 'cryptocurrency_logic.CryptocurrencyLogicAdapter'},
        {
            "import_path": "chatterbot.logic.BestMatch",
            "statement_comparison_function": "chatterbot.comparisons.levenshtein_distance",
            "response_selection_method": "chatterbot.response_selection.get_first_response"
        },
        {
            'import_path': 'chatterbot.logic.LowConfidenceAdapter',
            'threshold': 0.75,
            'default_response': 'I am sorry, but I do not understand.'
        },
    ],
    training_data=[
        'chatterbot.corpus.english.greetings',
        './data/'
    ],
)

# train chatterbot with corpus data and collect Q&As
chatbot.train(
    "chatterbot.corpus.english"
)

chatbot.train('./data/')

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    # calling chatterbot API to get the response
    answer = chatbot.get_response(msg.text)

    # save the question and answer into db
    record = CryptoCurrency(question=msg.text, answer=answer.text)
    session.add(record)
    session.commit()

    return answer.text

# reply to the user when question is asked
# wechat robot application
# need to scan your two-dimension code for wechat authentication

itchat.auto_login()
itchat.run()

