# Distributed Chat Application (Fault-Tolerant & Scalable)

This project implements a real-time distributed chat system using Python, Redis Pub/Sub, WebSockets, and Nginx load balancing.  
It demonstrates distributed architecture, fault tolerance, and scalable communication between clients.

## Features

- Multi-server WebSocket architecture
- Redis Pub/Sub for cross-server messaging
- Nginx as a load balancer
- Fault-tolerant client reconnection
- Real-time messaging
- Load testing with simulated clients

## Requirements

- Python 3.10+
- Redis server
- Nginx
- macOS or Linux (tested on macOS with Homebrew)

## How to Run

### 1. Start Redis

```bash
brew services start redis
```

### 2. Start Nginx

Ensure your `nginx.conf` contains:

```nginx
http {
    upstream chat_backend {
        server 127.0.0.1:6789;
        server 127.0.0.1:6790;
    }

    server {
        listen 8080;

        location / {
            proxy_pass http://chat_backend;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection "upgrade";
            proxy_set_header Host $host;
        }
    }
}
```

Then reload:

```bash
sudo nginx -s reload
```

### 3. Start Chat Servers

```bash
python -m server.run_server 6789
python -m server.run_server 6790
```

### 4. Start Chat Clients

```bash
python -m client.chat_client
```

### 5. Run Load Test (optional)

```bash
python simulator/load_test.py
```

## Redis Pub/Sub Model

Each server:
- Publishes incoming messages to a Redis channel
- Subscribes to that channel to receive messages from other servers
- Sends messages to its own WebSocket clients

## Fault Tolerance

- Clients reconnect automatically if a server goes down
- Nginx balances connections across available servers
- Redis acts as a central broadcast system

## Author

Oussama Hassine  
https://github.com/OussemaHassine