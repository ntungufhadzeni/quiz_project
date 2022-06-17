from service import create_bot
from train import train_with_csv, train_with_corpus

# create the bot
chatbot = create_bot()

# train
# train_with_corpus(chatbot, 'chatterbot.corpus.english')
train_with_csv(chatbot, './data/mental_health_faq.csv')