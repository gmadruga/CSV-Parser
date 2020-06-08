import json

import boto3
from chalice import Chalice
from chalice.app import SQSRecord
from chalicelib.src.parserCSV.abstract import AbstractPaser

S3 = boto3.client('s3', region_name='us-west-2')
app = Chalice(app_name='testeapi')
path = ''

@app.on_sqs_message('ParserLambdaCSV_SQS_PY')
def pathfinder(event):
    if isinstance(event, SQSRecord):
        record = json.loads(event.body)
    elif isinstance(event, str):
        record = json.loads(event)
    else:
        record = event

    AbstractPaser.getFileFromS3(path);

    return record


