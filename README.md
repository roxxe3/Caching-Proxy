# Caching-Proxy

A caching proxy server that caches responses from external APIs to improve performance and reduce load on the external servers. This server uses Redis for caching and Flask for handling HTTP requests.

project url = `https://roadmap.sh/projects/caching-server`

## Features

- Caches responses from external APIs in Redis.
- Returns cached responses for subsequent requests to the same URL.
- Provides a flag to clear the cache.
- Adds custom headers to responses to indicate cache hits or misses.

## Requirements

- Python 3.6+
- Redis server
- Flask
- Requests

## Installation

1. Clone the repository:

    ```sh
    git clone https://github.com/yourusername/caching-proxy.git
    cd caching-proxy
    ```

2. Install the required Python packages:

    ```sh
    pip install -r requirements.txt
    ```

3. Ensure you have a Redis server running. You can start a Redis server using Docker:

    ```sh
    docker run -d -p 6379:6379 redis
    ```

## Usage

Run the Flask app with the following command:

```sh
python3 cashing_proxy.py --host <host> --port <port> --origin <origin_url>
```

### Command-line Arguments

- `--host`: Host to run the app (default: `127.0.0.1`)
- `--port`: Port to run the app (default: `5000`)
- `--origin`: Base URL for the proxy
- `--clear-cache`: Clear the Redis cache before starting the app

### Example

```sh
python3 cashing_proxy.py --host 0.0.0.0 --port 8080 --origin https://api.example.com
```

This will start the Flask app on `http://0.0.0.0:8080` and proxy requests to `https://api.example.com`.
