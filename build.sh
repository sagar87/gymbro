#!/bin/sh
docker build -t sagar87/todo-backend:latest -f services/backend/Dockerfile.prod services/backend
docker push sagar87/todo-backend:latest

docker build -t sagar87/todo-client:latest -f services/client/Dockerfile.prod services/client
docker push sagar87/todo-client:latest