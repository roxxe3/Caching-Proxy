import redis
from flask import Flask, jsonify, make_response
import requests
import sys
import json
import argparse

redis_client = redis.Redis()
hit_or_miss = ""
app = Flask(__name__)

def get_cached(cache_key):
    """
    Retrieve data from Redis cache.
    """
    global hit_or_miss
    cached_data = redis_client.get(cache_key)
    if cached_data:
        hit_or_miss = "HIT"
        print(f"Cache hit for key: {cache_key}")
        try:
            return json.loads(cached_data.decode('utf-8'))
        except json.JSONDecodeError:
            print(f"Error decoding JSON for key: {cache_key}")
            return None
    return None

def set_cache(cache_key, data):
    redis_client.set(cache_key, data)

def fetch_data(cache_key, url):
    """
    Fetch data from cache or URL.

    This function attempts to retrieve data from a cache using the provided cache key.
    If the data is not found in the cache, it fetches the data from the specified URL,
    caches the result, and returns the data in JSON format.

    Args:
        cache_key (str): The key used to look up the data in the cache.
        url (str): The URL to fetch the data from if it's not found in the cache.

    Returns:
        dict: The data retrieved from the cache or URL in JSON format.

    Raises:
        Exception: If there is an error fetching the data or if the response is empty or invalid.
    """
    global hit_or_miss
    try:
        data = get_cached(cache_key)
        if data:
            return data
        req_data = request_data(url)
        if req_data and req_data.text.strip():
            data_to_cache = req_data.text
            set_cache(cache_key, data_to_cache)
            hit_or_miss = "MISS"
            return req_data.json()
        else:
            raise Exception("Empty response or invalid response")
    except Exception as error:
        print(f"Error fetching data: {error}")
        raise Exception("Failed to fetch data") from error

def request_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

@app.route('/favicon.ico')
def favicon():
    return '', 204

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def cashing_proxy(path):
    base_url_config = app.config.get('BASE_URL', '')
    cache_key = f"{base_url_config}/{path}"
    request_url = f"{base_url_config}/{path}"
    final_data = fetch_data(cache_key, request_url)
    
    response = make_response(jsonify(final_data))
    
    response.headers['X-Cache'] = hit_or_miss
    
    return response

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run Flask app with command-line arguments.")
    parser.add_argument('--host', default='127.0.0.1', help='Host to run the app')
    parser.add_argument('--port', type=int, default=5000, help='Port to run the app')
    parser.add_argument('--origin', default='', help='route url')
    parser.add_argument('--clear-cache', action='store_true', help='clear cache')

    args = parser.parse_args()
    if args.clear_cache:
        redis_client.flushdb()
        print("All cached data is deleted")
        sys.exit()
    app.config['BASE_URL'] = args.origin
    print(app.config['BASE_URL'])
    app.run(host=args.host, port=args.port, debug=True)