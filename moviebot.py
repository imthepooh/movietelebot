'''
This bot will send movie information based on title or list of movies based on search string

This used the open api provided by http://www.omdbapi.com/

'''
from telegram.ext import CommandHandler, Updater, Dispatcher, MessageHandler, Filters
import logging
import os
import json
import requests
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

logger = logging.getLogger(__name__)

def start(bot,update):
    greeting = 'Hello, how are you doing?\nSend me a message using one of the commands \n\n "/title <movie name>" \n "/search <keyword>" \n\n to get the movie information'
    bot.send_message(chat_id=update.message.chat_id,text=greeting)

def error(bot,update):
    # Log errors
    logger.warning('Update "%s" caused error "%s"', bot, update.error)

def title(bot,update):
    #declare variables to store required values
    c_id = update.message.chat_id
    m_txt = update.message.text.replace('/title','').lstrip().rstrip()
    
    if(m_txt == ''):
        bot.send_message(chat_id=c_id,text='Invalid movie title')
    else:
        # print("Received movie name: ",m_txt)
        bot.send_message(chat_id=c_id,text=callapi_title(m_txt))

def search(bot,update):
    #declare variables to store required values
    c_id = update.message.chat_id
    m_txt = update.message.text.replace('/search','').lstrip().rstrip()

    if(m_txt == ''):
        bot.send_message(chat_id=c_id,text='Invalid search string')
    else:
        bot.send_message(chat_id=c_id,text=callapi_search(m_txt))

def callapi_title(txt):
    api_base_url = 'http://www.omdbapi.com/?'
    api_key = os.getenv('OMAPI')
    api_url = api_base_url+'apikey='+api_key+'&t='+txt.replace(' ','+')
    response = requests.get(api_url)
    if(response.status_code == 200):
        resp_txt = json.loads(response.content.decode('utf-8'))
        # print("Recieved response: \n",resp_txt)
        if(resp_txt['Response'] == 'True'):
            framed_response = "Title: " + resp_txt['Title'] + "\n" + "Year: " + resp_txt['Year'] + "\n" + "Release Date: " + resp_txt['Released'] + "\n" + "Plot Summary: " + resp_txt['Plot'] + "\n"         
        else:
            framed_response = "Invalid Movie title"
    else:
        framed_response = "Something went wrong! Please try again"
    return(framed_response)

def callapi_search(txt):
    api_base_url = 'http://www.omdbapi.com/?'
    api_key = os.getenv("OMAPI")
    api_url = api_base_url+'apikey='+api_key+'&s='+txt.replace(' ','+')
    framed_response = 'Movies with the name "'+txt+'" in them: \n'
    response = requests.get(api_url)
    if(response.status_code == 200):
        resp_txt = json.loads(response.content.decode('utf-8'))
        # print("Recieved response: \n",resp_txt,"\n")
        # print('Search result:',resp_txt['Search'])
        if(resp_txt['Response']== 'True'):
            for t in resp_txt['Search']:
                framed_response += t['Title'] + '\n'
        else:
                framed_response = "No results found"
    else:
        framed_response = "Something went wrong! Please try again"
    return(framed_response)

def main():
    #Initialize the updater and dispatcher
    tok = os.getenv('MTOKEN')
    updater = Updater(token=tok)
    dispatcher = updater.dispatcher

    #Register the handlers
    start_handler = CommandHandler('start',start)
    dispatcher.add_handler(start_handler)

    title_handler = CommandHandler('title',title)
    dispatcher.add_handler(title_handler)

    search_handler = CommandHandler('search',search)
    dispatcher.add_handler(search_handler)

    # dispatcher.add_handler(MessageHandler(Filters.text,checkText))

    dispatcher.add_error_handler(error)

    #start polling for updates
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()
    
