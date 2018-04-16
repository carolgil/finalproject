import requests
from bs4 import BeautifulSoup
import sys
import sqlite3
import json

# create trip.db database
# contains 2 tables: Activities and ActivityInfo
DBNAME = 'trip.db'

# init db
conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# Drop tables
statement1 = '''
    DROP TABLE IF EXISTS 'Activities';
'''

statement2 = '''
    DROP TABLE IF EXISTS 'ActivityInfo';
'''

cur.execute(statement1)
cur.execute(statement2)

conn.commit()

query1 = '''
    CREATE TABLE 'Activities' (
        'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
        'State' TEXT,
        'Attraction' TEXT,
        'Location' TEXT,
        'URL' TEXT
    );
'''

query2 = '''
    CREATE TABLE 'ActivityInfo' (
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
    'Title' TEXT,
    'Type' TEXT,
    'Rating' INTEGER,
    'NumReviews' INTEGER
    );
'''


cur.execute(query1)
cur.execute(query2)

conn.commit()
conn.close()

# Cache STATE ACTIVITIES
# on startup, try to load the cache from file
CACHE_FNAME = 'cache.json'
CACHE_FNAME2 = 'cache2.json'
try:
    cache_file = open(CACHE_FNAME, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION = {}

try:
    cache_file = open(CACHE_FNAME2, 'r')
    cache_contents = cache_file.read()
    CACHE_DICTION2 = json.loads(cache_contents)
    cache_file.close()

# if there was no file, no worries. There will be soon!
except:
    CACHE_DICTION2 = {}

def get_unique_key(url, code):
    full_url = url + code
    return full_url

# The main cache function: it will always return the result for this
# url+params combo. However, it will first look to see if we have already
# cached the result and, if so, return the result from cache.
# If we haven't cached the result, it will get a new one (and cache it)

def make_request_using_cache(url, code):
    unique_ident = get_unique_key(url, code)

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION:
        # print("Getting cached data...")
        return CACHE_DICTION[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data

        full_url = url + code
        resp = requests.get(full_url)

        CACHE_DICTION[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION)
        fw = open(CACHE_FNAME,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION[unique_ident]




# Cache 2
def make_request_using_cache2(url):
    unique_ident = url

    ## first, look in the cache to see if we already have this data
    if unique_ident in CACHE_DICTION2:
        # print("Getting cached data...")
        return CACHE_DICTION2[unique_ident]

    ## if not, fetch the data afresh, add it to the cache,
    ## then write the cache to file
    else:
        # print("Making a request for new data...")
        # Make the request and cache the new data

        resp = requests.get(url)

        CACHE_DICTION2[unique_ident] = resp.text
        dumped_json_cache = json.dumps(CACHE_DICTION2)
        fw = open(CACHE_FNAME2,"w")
        fw.write(dumped_json_cache)
        fw.close() # Close the open file
        return CACHE_DICTION2[unique_ident]


# need state code in link to scrape page
state_code_dict = {
    'Alabama': 'g28922',
    'Alaska' : 'g28923',
    'Arizona' : 'g28924',
    'Arkansas' : 'g28925',
    'California' : 'g28926',
    'Colorado' : 'g28927',
    'Connecticut' : 'g28928',
    'Delaware' : 'g28929',
    'Florida' : 'g28930',
    'Georgia' : 'g28931',
    'Hawaii' : 'g28932',
    'Idaho' : 'g28933',
    'Illinois' : 'g28934',
    'Indiana' : 'g28935',
    'Iowa' : 'g28936',
    'Kansas' : 'g28937',
    'Kentucky' : 'g28938',
    'Louisiana' : 'g28939',
    'Maine' : 'g28940',
    'Maryland' : 'g28941',
    'Massachusetts' : 'g28942',
    'Michigan' : 'g28943',
    'Minnesota' : 'g28944',
    'Mississippi' : 'g28945',
    'Missouri' : 'g28946',
    'Montana' : 'g28947',
    'Nebraska' : 'g28948',
    'Nevada' : 'g28949',
    'New_Hampshire' : 'g28950',
    'New_Jersey' : 'g28951',
    'New_Mexico' : 'g28952',
    'New_York' : 'g28953',
    'North_Carolina' : 'g28954',
    'North_Dakota' : 'g28955',
    'Ohio' : 'g28956',
    'Oklahoma' : 'g28957',
    'Oregon' : 'g28958',
    'Pennsylvania' : 'g28959',
    'Rhode_Island' : 'g28960',
    'South_Carolina' : 'g28961',
    'South_Dakota' : 'g28962',
    'Tennessee' : 'g28963',
    'Texas' : 'g28964',
    'Utah' : 'g28965',
    'Vermont' : 'g28966',
    'Virginia' : 'g28967',
    'Washington' : 'g28968',
    'West_Virginia' : 'g28971',
    'Wisconsin' : 'g28972',
    'Wyoming' : 'g28973'
}

class State:
    def __init__(self, name, attraction, location, url=None):
        self.name = name
        self.attraction = attraction
        self.location = location
        self.url = url

    def __str__(self):
        str_ = self.name + ": " + self.attraction + " in " + self.location
        return str_

class Activity:
    def __init__(self, title, type, rating, num_reviews):
        self.title = title
        self.type = type
        self.rating = rating
        self.num_reviews = num_reviews


conn = sqlite3.connect(DBNAME)
cur = conn.cursor()



def init_db():
    for state in state_code_dict:
        baseurl = 'https://www.tripadvisor.com/Attractions-'
        state_code = state_code_dict[state]
        full_url = baseurl + state_code
        page_text = make_request_using_cache(baseurl, state_code)
        soup = BeautifulSoup(page_text, 'html.parser')
        todo = soup.find_all(class_='listing_title')
        count = 0
        for t in todo:
            if count < 3:
                if t.find('a') is not None:
                    a = t.find('a').text
                else:
                    a = "None"
                url = "https://www.tripadvisor.com" + t.find('a')['href']
                if t.find('span') is not None :
                    l = t.find('span').text
                else:
                    l = "None"
                insertion = (None, state, a, l, url)
                statement = 'INSERT INTO "Activities" '
                statement += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, insertion)
                count = count + 1
                text = make_request_using_cache2(url)
                ramen = BeautifulSoup(text, 'html.parser')
                detail = ramen.find_all(class_='detail')
                popularity = ramen.find_all(class_='header_popularity')
                reviews = ramen.find_all(class_='header_rating')
                for d,p,r in zip(detail,popularity,reviews):
                    if d.find('a') is not None:
                        type = d.find('a').text
                    else:
                        type = "None"
                    if p.find('span') is not None:
                        rating = p.find('span').text[1:]
                    else:
                        rating = 0
                    rev = r.find('a')
                    if rev.find('span') is not None:
                        num_reviews = rev.find('span').text
                    else:
                        num_reviews = 0
                insert = (None, a, type, rating, num_reviews)
                statement = 'INSERT INTO "ActivityInfo" '
                statement += 'VALUES (?, ?, ?, ?, ?)'
                cur.execute(statement, insert)
            else:
                break
    conn.commit()



if __name__ == "__main__":
    # init_db()

    entered = input('Enter command (or "help" for options): ')
    entered = entered.split()
    command = entered[0]

    while (command != "exit"):
        if command == "exit" :
            print("Bye!")

        # FIRST GRAPH
        # creates bar chart of activity rankings in state specified
        elif command == "rankings":
            pass

        else:
            print("Bad input :( try again!")

        entered = input('Enter command (or "help" for options): ')
        entered = entered.split()
        command = entered[0]


    if command == "exit" :
        print("Bye!")
