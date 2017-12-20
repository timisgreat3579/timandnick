import hashlib,uuid,random,boto3

session = boto3.resource('dynamodb',
    aws_access_key_id='AKIAIOPUXE2QS7QN2MMQ',
    aws_secret_access_key='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',
    region_name="ca-central-1"
)
table = session.Table('highscores')

def update_item(table):
    pass
