import os
import logging
import json

try:
    from db import get_ddb_connection, Fridge
except:
    # If it gets here it's because we are performing a unit test. It's a common error when using lambda layers
    # Here is an example of someone having a similar issue:
    # https://stackoverflow.com/questions/69592094/pytest-failing-in-aws-sam-project-due-to-modulenotfounderror
    from dependencies.python.db import get_ddb_connection, Fridge

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class FridgHandler:
    @staticmethod
    def get_fridge_id(event: dict):
        """
        Gets the fridge_id from the event dictionary
        """
        fridge_id = None
        if event["pathParameters"] is not None:
            fridge_id = event["pathParameters"].get("fridge_id", None)
        return fridge_id

    @staticmethod
    def lambda_handler(event: dict, ddbclient: "botocore.client.DynamoDB") -> dict:
        """
        Extracts the necessary data from events dict, and executes a function corresponding
        to the event httpMethod
        """
        httpMethod = event.get("httpMethod", None)
        fridge_id = FridgHandler.get_fridge_id(event)
        db_response = None
        if httpMethod == "GET":
            if fridge_id:
                db_response = Fridge(db_client=ddbclient).get_item(fridge_id)
            else:
                raise ValueError(f"Query Fridges API Not Yet Developed")
        elif httpMethod == "POST":
            pass
        else:
            raise ValueError(f'Invalid httpMethod "{httpMethod}"')
        return db_response.api_format()


def lambda_handler(
    event: dict, context: "awslambdaric.lambda_context.LambdaContext"
) -> dict:
    env = os.environ["Environment"]
    ddbclient = get_ddb_connection(env)
    return FridgHandler.lambda_handler(event, ddbclient)
