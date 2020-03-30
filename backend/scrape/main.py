import os
from google.cloud import spanner

spanner_client = spanner.Client()
spanner_instance = spanner_client.instance(
    os.environ.get('Spanner_Instance', 'NOT SET'))

spanner_database = spanner_instance.database(
    os.environ.get('Spanner_Database', 'NOT SET'))


def insertMockData(transaction):
    transaction.execute_update('DELETE FROM location WHERE true')
    transaction.execute_update(
        "INSERT location (locId, name, phone, city, state, country, days, hours) VALUES (0, 'name', 'phone', 'city', 'state', 'country', 'days', 'hours')")


def handler(request):
    """Responds to any HTTP request.
    Args:
        request (flask.Request): HTTP request object.
    Returns:
        The response text or any set of values that can be turned into a
        Response object using
        `make_response <http://flask.pocoo.org/docs/1.0/api/#flask.Flask.make_response>`.
    """
    spanner_database.run_in_transaction(insertMockData)

    request_json = request.get_json()
    if request.args and 'message' in request.args:
        return request.args.get('message')
    elif request_json and 'message' in request_json:
        return request_json['message']
    else:
        return f'Hello World!'
