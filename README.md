# Distributed Chat Application (Fault-Tolerant & Scalable)

This project implements a real-time distributed chat system using Python, Redis Pub/Sub, WebSockets, and Nginx load balancing.  
It demonstrates distributed architecture, fault tolerance, and scalable communication between clients.
Clients connect to servers via Nginx, when a client send a message, the message reaches the server, the server publishes it to Redis, Redis broadcast it to subscribed servers, subscribed servers send it to their connected clients. When a server dies, the client detects that instantly and tries to reconnect via Nginx who would reassign it to another available server. This architecture ensures uninterrupted communication and resilience in a multi-server environment.

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
- Tested on macOS with Homebrew

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
        #more servers, more ports here
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
#you can run as much servers as you want using different ports, but these ports needs to be mentioned in the nginx.conf file.
```

### 4. Start Chat Clients

```bash
python client/chat_client.py
#you can run as much clients as you want without mentioning any port, they will all connect to Nginx via 8080 port, in which the latest will forward them to available servers.
```

### 5. Run Load Test (optional)

```bash
python simulator/load_test.py
#this will show you how in a real-world, clients connect, send messages, disconnect and reconnect again to different servers.
#in the file, you can change the amount of simulated clients and the interval of messages sent.
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

## Final thoughts 

This project was developed to satisfy academic requirements for a Distributed Systems course. While fully functional, several extensions can enhance it further, including:

- Adding persistent usernames
- Supporting private messaging between clients
- Creating separate chat rooms or channels
- Building a GUI for improved user experience
