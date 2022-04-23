import json
import urllib3
from helpers import * 


def handle_sqs_event(event, context):
    http = urllib3.PoolManager()
    top10_films_raw = event['Records'][0]['body']
    top10_films = json.loads(top10_films_raw)
    enriched_data = []
    
    for s3_film_data in top10_films:
        id = s3_film_data['id']
        endpoint = get_endpoint_for_id(id)
        response = http.request('GET', endpoint)

        api_film_data = json.loads(response.data)
        enriched_film_data = api_film_data | s3_film_data
        
        for key in keys_to_remove:
            enriched_film_data.pop(key)
    
        enriched_data.append(enriched_film_data)
        
    # Not updating ranks based on updated ratings.
    output_json = json.dumps(enriched_data)
    
    upload_json_to_s3(output_json)
