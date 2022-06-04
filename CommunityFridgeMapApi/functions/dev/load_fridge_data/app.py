import os
import json
import logging
from botocore.exceptions import ClientError
from db import get_ddb_connection
from db import Fridge
logger = logging.getLogger()
logger.setLevel(logging.INFO)

FRIDGE_DATA = [
                {
                    'fridge_state': 'NY',
                    'display_name': 'The Friendly Fridge',
                    'address': '1046 Broadway Brooklyn, NY 11221',
                    'instagram': 'https://www.instagram.com/thefriendlyfridge/',
                    'lat': '40.695190',
                    'long': '-73.932180'
                },
                {
                    'fridge_state': 'NY',
                    'display_name': '2 Fish 5 Loaves Fridge',
                    'address': '63 Whipple St, Brooklyn, NY 11206',
                    'instagram': 'https://www.instagram.com/2fish5loavesfridge/',
                    'lat': '40.701730',
                    'long': '-73.944530'
                }
            ]


FRIDGE_CHECK_IN_DATA = []
FRIDGE_HISTORY_DATA = []

def lambda_handler(event: dict, context: 'awslambdaric.lambda_context.LambdaContext') -> dict:
    db_client = get_ddb_connection(env=os.environ['Environment'])
    try:
        for fridge in FRIDGE_DATA:
            Fridge(fridge=fridge, db_client=db_client).add_fridge()
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Filled DynamoDB',
            }),
        }

    except db_client.exceptions.ResourceNotFoundException as e:
        logging.error('Table does not exist')
        raise e
    except db_client.exceptions.ConditionalCheckFailedException as e:
        logging.error('Fridge already exists')
        raise e
    except ClientError as e:
        logging.error('Unexpected error')
        raise e

