# Secure Publish--Subscribe Notification Service

## Overview

This project implements a **secure publish--subscribe notification
system** using **low-level TCP socket programming with SSL/TLS
encryption**. The system allows multiple clients to subscribe to topics
and receive real-time notifications published by publishers.

The architecture demonstrates concepts of: - Network socket
programming - Secure communication using SSL/TLS - Concurrent client
handling - Topic-based event routing - Real-time messaging systems

This project is designed as a **Computer Networks socket programming
mini project**.

------------------------------------------------------------------------

# System Architecture

The system follows a **broker-based publish--subscribe architecture**.

Publisher → Server (Broker) → Subscribers

The **server acts as the message broker** responsible for: - Managing
topics - Maintaining subscriber lists - Routing messages to appropriate
subscribers

Components:

1.  **Server (Broker)**
    -   Handles client connections
    -   Manages topic subscriptions
    -   Routes published messages
2.  **Subscriber Client**
    -   Subscribes to topics
    -   Receives notifications
3.  **Publisher Client**
    -   Publishes messages to topics

------------------------------------------------------------------------

# Features

-   Secure TCP communication using **SSL/TLS**
-   Multi-client concurrency using **threads**
-   Topic-based subscription management
-   Real-time message delivery
-   Multiple publishers and subscribers supported
-   Simple custom messaging protocol

------------------------------------------------------------------------

# Project Structure

    pubsub-notification-service
    │
    ├── server.py        # Broker server
    ├── client.py        # Subscriber client
    ├── publisher.py     # Publisher client
    ├── server.crt       # SSL certificate
    ├── server.key       # SSL private key
    └── README.md        # Project documentation

------------------------------------------------------------------------

# Communication Protocol

The system uses a simple text-based protocol.

Client Commands

SUBSCRIBE `<topic>`{=html} PUBLISH `<topic>`{=html} `<message>`{=html}
EXIT

Server Responses

SUBSCRIBED `<topic>`{=html} MESSAGE `<topic>`{=html} `<message>`{=html}
ERROR `<message>`{=html}

Example:

Subscriber → SUBSCRIBE sports\
Publisher → PUBLISH sports India won\
Server → MESSAGE sports India won

------------------------------------------------------------------------

# SSL/TLS Security

The system uses **SSL encryption** to secure all communications.

Benefits: - Encrypts messages - Prevents packet sniffing - Protects data
integrity - Authenticates the server

A self-signed certificate is used for development.

------------------------------------------------------------------------

# Generating SSL Certificates

Run the following command to generate SSL certificates:

    openssl req -new -x509 -days 365 -nodes -out server.crt -keyout server.key -subj "/C=IN/ST=KA/L=Bangalore/O=PubSub/CN=localhost"

This generates:

-   server.crt → Public certificate
-   server.key → Private key

------------------------------------------------------------------------

# Installation

Requirements:

-   Python3

Check Python:

    python3 --version

------------------------------------------------------------------------

# Running the System

## Step 1: Start the Server

    python3 server.py

Expected Output:

Server running on port 5000

------------------------------------------------------------------------

## Step 2: Start Subscriber Clients

Open a new terminal:

    python3 client.py

Example:

Enter topic to subscribe: sports

------------------------------------------------------------------------

## Step 3: Start Publisher

    python3 publisher.py

Example:

Enter topic: sports\
Enter message: India won

------------------------------------------------------------------------

# Example Workflow

Subscriber 1 subscribes:

SUBSCRIBE sports

Subscriber 2 subscribes:

SUBSCRIBE sports

Publisher publishes:

PUBLISH sports Goal scored

Subscribers receive:

(New Message Received)\[sports\] Goal scored

------------------------------------------------------------------------

# Performance Testing

The system can be evaluated under different loads:

  Clients   Description
  --------- ----------------
  5         Normal usage
  10        Moderate load
  20+       Stress testing

Metrics measured: - Message latency - Throughput - System scalability

------------------------------------------------------------------------

# Real World Applications

This architecture is used in many real-world systems:

-   YouTube notification systems
-   Stock market alerts
-   Chat messaging platforms
-   News alert services

------------------------------------------------------------------------

# Learning Outcomes

This project demonstrates:

-   TCP socket programming
-   Secure networking with SSL/TLS
-   Client-server architecture
-   Concurrent programming
-   Event-driven messaging systems

------------------------------------------------------------------------

# Author

Piyush A Patel
