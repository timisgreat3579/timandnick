import pip
import importlib
new_package = importlib.util.find_spec('boto3')
found = new_package is not None
if not found:
    pip.main(['install','boto3'])
import boto3

session = boto3.resource('dynamodb',
    aws_access_key_id='AKIAIOPUXE2QS7QN2MMQ',
    aws_secret_access_key='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',
    region_name="ca-central-1"
)
table = session.Table('people')
print(table.scan('peopleid'))
