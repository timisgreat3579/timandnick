import pip
import importlib
new_package = importlib.util.find_spec('boto3')
found = new_package is not None
if not found:
    pip.main(['install','boto3'])
import boto3

session = boto3.resource('dynamodb',
   

table = session.Table('people')
print(table.scan('peopleid'))
