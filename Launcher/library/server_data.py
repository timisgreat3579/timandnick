from .loading_screen import session_var
from configparser import ConfigParser
from boto3.dynamodb.conditions import Key, Attr
launcher_config = ConfigParser()
launcher_config.read('./data/config.ini')
user = launcher_config.get('USER','username')
user = 'nickiscool123'

session = session_var
people_table = session.Table('people')

def get_players(query):
    response = people_table.scan()
    names = []
    for i in response['Items']:
        name = i['peopleid']
        if query in name.lower() and len(query) is not 0:
            names.append(name)
        elif len(query) is 0:
            names.append(name)

    return names

def get_table_data(data):
    response = people_table.query(KeyConditionExpression=Key('peopleid').eq(user))
    for i in response['Items']: names = i[data]
    if user in names: names.remove(user)
    return names 


