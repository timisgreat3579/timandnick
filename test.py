def addFriends(friend):
    #user_login
    
    #Update friends
    table = session.Table('peopleid')
    response = table.get_item(
        Key={
            'peopleid': user_login
        }
    )
    nFriends = response['Item']['friends']
    nFriends.append(friend)
    
    response = table.update_item(
        Key={
            'peopleid':user_login
        },
        UpdateExpression="set " + 'friends' + " = :r",
        ExpressionAttributeValues={
            ':r': nFriends,
        }
    )

    response = table.get_item(
        Key={
            'peopleid': friend
        }
    )
    nFreinds = response['Item']['friends']
    nFreinds.append(user_login)
    
    response = table.update_item(
        Key={
            'peopleid':friend
        },
        UpdateExpression="set " + 'friends' + " = :r",
        ExpressionAttributeValues={
            ':r': nFreinds,
        }
    )

    #update requests

    response = table.get_item(
        Key={
            'peopleid': user_login
        }
    )
    oldRequests = response['Item']['requests']
    x = oldRequests.index(user_login)
    del oldRequests[x]
    
    response = table.update_item(
        Key={
            'peopleid':user_login
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )

    response = table.get_item(
        Key={
            'peopleid': friend
        }
    )
    oldRequests = response['Item']['requests']
    x = oldRequests.index(user_login)
    del oldRequests[x]
    
    response = table.update_item(
        Key={
            'peopleid':friend
        },
        UpdateExpression="set " + 'requests' + " = :r",
        ExpressionAttributeValues={
            ':r': oldRequests,
        }
    )
    
