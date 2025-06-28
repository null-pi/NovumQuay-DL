#!/bin/bash

# Set the default value for PRODUCTION if not provided
PRODUCTION=${PRODUCTION:-"false"}

# Go to the directory where the FastAPI application is located
cd /app/fastapi_app

# Run the FastAPI application based on the value of PRODUCTION
if [ -z "$PRODUCTION" ] || [ "$PRODUCTION" = "false" ]; then
    fastapi dev --host 0.0.0 --port 8000
elif [ "$PRODUCTION" = "true" ]; then
    fastapi run --host 0.0.0.0 --port 8000
else
    echo "Invalid value for PRODUCTION: $PRODUCTION"
    exit 1
fi


