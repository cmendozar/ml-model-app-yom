#!/bin/bash

IMAGE_NAME="yom-app"
CONTAINER_NAME="yom-app-container"
PORT=8000

# Set BUILD to true or false as needed
BUILD=true

# Check if there is a container using the specified port and stop/remove it
EXISTING_CONTAINER_ID=$(docker ps -q --filter "publish=$PORT")

if [ -n "$EXISTING_CONTAINER_ID" ]; then
    echo "Stopping and removing the container using port $PORT..."
    docker stop $EXISTING_CONTAINER_ID
    docker rm $EXISTING_CONTAINER_ID
fi

if [ "$BUILD" = true ]; then
  echo "Building the Docker image..."
  docker build -t $IMAGE_NAME .
else
  echo "Skipping build. Using existing Docker image."
fi

# Check if a container with the specified name already exists and remove it
if [[ "$(docker ps -aq -f name=$CONTAINER_NAME)" ]]; then
    echo "Removing existing container with name $CONTAINER_NAME..."
    docker rm -f $CONTAINER_NAME
fi

echo "Running a new container..."
docker run -d --name $CONTAINER_NAME -p $PORT:$PORT $IMAGE_NAME

echo "Container is up and running on port $PORT"

# Uncomment the following line to test the predict-song endpoint after the container is up
# curl -X POST http://localhost:$PORT/predict-song -H "Content-Type: application/json" -d '{"data": {"popularity": 68, "danceability": 0.826, "energy": 0.704, "key": 9, "loudness": -7.527, "mode": 1, "speechiness": 0.117, "acousticness": 0.189, "instrumentalness": 4.8e-05, "liveness": 0.0617, "valence": 0.741, "tempo": 94.013, "duration": 205000, "id_new": 1}}'
