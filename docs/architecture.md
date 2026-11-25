# DistroHub - System Architecture

## 1. Overview

DistroHub is a web platform for provisioning and managing isolated
Linux environments through a browser-based terminal.

The initial version will support Ubuntu, Debian and Alpine containers.

## 2. Technology Stack

- Frontend: React + Vite
- Backend: Python + FastAPI
- Container runtime: Docker Engine
- Container integration: Docker SDK for Python
- Terminal: xterm.js
- Communication: HTTP and WebSockets
- Database: PostgreSQL
- Infrastructure: Docker Compose
- Reverse proxy: Nginx

## 3. High-Level Architecture

Browser
   |
   v
React Frontend
   |
   | HTTP / WebSocket
   v
FastAPI Backend
   |
   +----------> PostgreSQL
   |
   v
Docker SDK
   |
   v
Docker Engine
   |
   +----------> Ubuntu Container
   +----------> Debian Container
   +----------> Alpine Container

## 4. Environment Lifecycle

1. User authenticates.
2. User selects a Linux distribution.
3. Frontend sends an environment creation request.
4. Backend validates the request and user permissions.
5. Backend provisions a container using Docker SDK.
6. Backend stores environment metadata in PostgreSQL.
7. Frontend displays the environment status.
8. User connects to the environment terminal.
9. User can stop, restart or delete the environment.

## 5. Terminal Communication

1. Browser terminal uses xterm.js.
2. Frontend establishes an authenticated WebSocket connection.
3. Backend verifies the user owns the requested environment.
4. Backend attaches to a Docker exec session.
5. Terminal input is forwarded to the container.
6. Container output is streamed back to the browser.

## 6. Data Management

PostgreSQL stores:
- User accounts
- Environment metadata
- Container identifiers
- Distribution information
- Environment status
- Creation timestamps

Docker volumes will provide persistent user workspace storage.

## 7. Security Principles

- Never expose the Docker API directly to users.
- Never mount the Docker socket inside user containers.
- Do not run user containers in privileged mode.
- Enforce authentication and ownership checks.
- Apply CPU and memory limits.
- Restrict container capabilities and network access.
- Validate all user-controlled inputs.
- Do not construct shell commands by concatenating user input.
- Treat Docker Engine access as highly privileged.

The backend is a trusted control-plane component. Access to the
Docker socket must be restricted to this component.

A single Docker host is suitable for local development, not by
itself a sufficient security boundary for a public multi-user service.

## 8. Initial MVP Scope

The first release will provide:

- User registration and login
- Linux environment provisioning
- Ubuntu, Debian and Alpine support
- Browser-based terminal
- Start, stop and delete operations
- Persistent workspace storage
- Environment status dashboard

Advanced graphical desktops, Kubernetes orchestration and
multi-host provisioning are outside the initial MVP scope.
