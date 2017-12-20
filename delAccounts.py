#SERVER SCRIPT - TIM RUSCICA
#Server Script for deleting accounts
#If an accounts email has not been verified within 24 hours it will be automatically deleted

import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr
from botocore.exceptions import ClientError
from datetime import datetime

def readAll():
    global table
    session = boto3.resource('dynamodb',
    aws_access_key_id='AKIAIOPUXE2QS7QN2MMQ',
    aws_secret_access_key='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',
    region_name="ca-central-1"
    )
    table = session.Table('people')

    response = table.scan()
    li = []
    for i in response['Items']:
        currentTime = str(datetime.now())
        date = i['datetime']
        time = date.split()
        time = time[1].split(':')
        cur = currentTime.split()
        cur = cur[1].split(':')
        if int(cur[0]) > int(time[0]) + 2: 
            li.append(i['peopleid'])

    deleteUser(li)
    
def deleteUser(usrList):
    for usr in usrList:
        response = table.delete_item(
            Key={
                'peopleid': usr
                }   
            )
readAll()
