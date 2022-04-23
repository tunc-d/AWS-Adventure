import boto3


"""
Since handling data inconsistencies is out of scope, I'm giving precedence to
the data from the omdb API in case of duplicates/related fields. 

"""
keys_to_remove = ['title', 'imdbID', 'image', 'crew', 'year','imDbRatingCount', 
'imDbRating']
api_key = "6e53dc85"


def get_endpoint_for_id(id):
    return f"https://www.omdbapi.com/?apikey={api_key}&i={id}"
    

def upload_json_to_s3(json_data):
    s3_client = boto3.client('s3')
    bucket = 'enriched-films-bucket'
    
    # Not generating unique filename as S3 bucket will use versioning
    filename = 'enriched_films.json'
    
    bytes_to_upload = bytes(json_data.encode('UTF-8'))
    s3_client.put_object(Bucket=bucket, Key=filename, Body=bytes_to_upload)
