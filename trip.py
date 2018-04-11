import requests
from bs4 import BeautifulSoup
import sys
import sqlite3


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
        'Location' TEXT
    );
'''

query2 = '''
    CREATE TABLE 'ActivityInfo' (
    'Id' INTEGER PRIMARY KEY AUTOINCREMENT
    )
'''


cur.execute(query1)
cur.execute(query2)

conn.commit()
conn.close()




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

activities = []
location = []

conn = sqlite3.connect(DBNAME)
cur = conn.cursor()

# TPut state activities into db table
for entry in state_code_dict:
    url = "https://www.tripadvisor.com/Attractions-" + state_code_dict.get(entry)
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'html.parser')
    todo = soup.find_all(class_='listing_title')
    for t in todo:
        if t.find('a') is not None:
            a = t.find('a').text
        else:
            a = "None"
        if t.find('span') is not None :
            l = t.find('span').text
        else:
            l = "None"
        insertion = (None, entry, a, l)
        statement = 'INSERT INTO "Activities" '
        statement += 'VALUES (?, ?, ?, ?)'
        cur.execute(statement, insertion)

# url = "https://www.tripadvisor.com/Attractions-" + state_code_dict.get('Michigan')
# html = requests.get(url).text
# soup = BeautifulSoup(html, 'html.parser')
# todo = soup.find_all(class_='listing_title')
# for t in todo:
#     a = t.find('a').text
#     l = t.find('span').text
#     insertion = (None, 'Michigan', a, l)
#     statement = 'INSERT INTO "Activities" '
#     statement += 'VALUES (?, ?, ?, ?)'
#     cur.execute(statement, insertion)

conn.commit()
conn.close()

# for s,a,l in zip(state_code_dict,activities,location):
#     print(a)
#     print(l)
#     insertion = (None, s, a, l)
#     statement = 'INSERT INTO "Activities" '
#     statement += 'VALUES (?, ?, ?, ?)'
#     cur.execute(statement, insertion)



if __name__ == "__main__":
    pass
    # entered = input('Enter command (or "help" for options): ')
    # entered = entered.split()
    # command = entered[0]
    #
    # while (command != "exit"):
    #     if command == "exit" :
    #         print("Bye!")
    #
    #     elif command == "activities":
    #         get_activities(entered)
