import json
import boto3


def get_top_10():
    s3_client = boto3.client('s3')
    
    bucket = "top-movies"
    key = "Top250Movies.json"
    
    response = s3_client.get_object(Bucket=bucket, Key=key)
    content = response['Body']
    json_data = json.loads(content.read())
    
    films = json_data['items']
    
    """ 
    Getting top 10 ranked movies. Working on the assumption that the input JSON
    will start from rank 1 and increment from there
    """
    return films[:10]


def queue_message(content):
    sqs_client = boto3.client('sqs')
    response = sqs_client.send_message(
        QueueUrl="https://sqs.eu-central-1.amazonaws.com/459727908782/FilmQueue",
        MessageBody=json.dumps(content)
        )
    
    return {
        'statusCode': response["ResponseMetadata"]["HTTPStatusCode"],
        'body': json.dumps(response["ResponseMetadata"])
    }


def get_data_and_queue_message(event, context):
    return queue_message(get_top_10())