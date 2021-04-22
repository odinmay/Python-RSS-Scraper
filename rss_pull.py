import datetime
import logging
import os
import sys
import yagmail
import feedparser

#CHANGE THIS
default_email = 'odinmerlinmay@gmail.com'

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(name)s %(levelname)-4s : %(message)s',
                    filename='main.log',filemode='w')


#python filename emails.txt

def start():
    scraper = Scraper()
    scraper.scrub()
    scraper.build_file()
    try:
        argument = sys.argv[1]
        get_info(argument)
    except:
        send_email(default_email)


def send_email(user_email):
    '''Sends completed file to passed email address at the end of runtime'''
    receiver=user_email
    body = "News | Blog Posts | Articles on Python \n brought to you by Odin May"
    filename = str(datetime.date.today()) + '.txt'
    yag=yagmail.SMTP(default_email)
    if(isinstance(receiver,list)):
        for emails in receiver:
            yag.send(to=emails,subject="Odins Python Newsletter",contents=body,attachments=filename)
            logging.info("Email Sent to " + emails)
    else:
        yag.send(to=receiver, subject="Odins Python Newsletter", contents=body, attachments=filename)
        logging.info("Email Sent to " + receiver)


def get_info(args):
    input_type = args[-3:]
    if input_type == "com":
        send_email(args)
    elif input_type == "txt":
        while not os.path.isfile(args):
            args = input("Whoops! No such file! Please enter the name of the file you'd like to use.")
        my_file = open(args, "r")
        content = my_file.read()
        content_list = content.split(",")
        send_email(content_list)
    else:
        logging.info("Error Obtaining Input")


class Scraper:
    def __init__(self):
        '''Sources to parse and containers for parsed data'''
        self.sources = {'Make Use Of' : 'https://www.makeuseof.com/rss',
                        'Planet Python' : 'https://planetpython.org/rss20.xml',
                        'Python Library' : 'http://www.blog.pythonlibrary.org/feed/',
                        'Finxster' : 'http://blog.finxter.com/feed',
                        'Real Python' : 'https://realpython.com/atom.xml?format=xml',
                        'Python.org' : 'http://blog.python.org/feeds/posts/default',
                        'Medium' : 'https://medium.com/feed/python4you',
                        'Talk Python to Me' : 'https://talkpython.fm/episodes/rss',
                        '' : ''}
        self.titles = []
        self.links = []
        logging.info('Scraper Initialized')

    def scrub(self):
        '''Iterating over sources and pulling nested data, saving to containers'''
        for k,v in self.sources.items():
            parsed_data = feedparser.parse(v)
            logging.info(v + " Scraped")
            for x in range(len(parsed_data['entries'])):
                self.titles.append(str(parsed_data['entries'][x]['title']))
                self.links.append((parsed_data['entries'][x]['link']))

    def build_file(self):
        '''Creating a text document with each title and link'''
        with open(str(datetime.date.today()) + '.txt', 'w', encoding='utf-8') as file:
            combined = zip(self.titles,self.links)
            for x in combined:
                file.write(x[0] + '\n' + x[1] + '\n\n')
        logging.info('File Created')


if __name__ == '__main__':
    start()
