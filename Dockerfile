# Use a lightweight official Python image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (if needed for some Python packages)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (better Docker caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Set environment variables (optional, for IGDB credentials, etc., tweak as needed)
ENV PYTHONUNBUFFERED=1

# Default command (interactive CLI or runner)
CMD ["python", "main.py"]

#Build docker image
#docker build -t top-game-sorter .

#Run app
#docker run -it --rm \
#  -v $(pwd)/data:/app/data \
#  top-game-sorter
#-it keeps it interactive (needed since your CLI asks for input).
#--rm removes the container after exit.
#-v $(pwd)/games.db:/app/games.db → mounts your local games.db file into the container at /app/games.db.
#Any changes inside the container persist to your host file.
#For windows powershell use:
#docker run -it --rm `
#  -v ${PWD}\games.db:/app/games.db `
#  top-game-sorter

#Docker compose
#docker-compose up --build
#If testing: docker compose build --progress=plain --no-cache
#--progress=plain -> shows each build step in plain text (instead of "fancy" UI)
#--no-cache: forces everything to rebuild, so see every step

#docker-compose up → starts all services (app, mongo, mongo-express). Good for your full stack.
#docker-compose run → starts only the service you specify. Useful for running the app interactively or running 
#commands inside it without starting everything else.

#TO RUN THE IMAGE:
#AFTER HAVING MADE ANY PROJECT CHANGES, WILL WANT TO BUILD:
#First: docker-compose build
#Then: docker-compose up -d mongo mongo-express (To have mongo set up in the background)
#Then for interactive input: docker-compose run --rm -it app 
#--rm = remove container when done
#-it = interactive terminal (so input() works)
#IF JUST RUNNING AGAIN, JUST SKIP THE BUILD STEP

#TO PUSH CHANGES TO DOCKER REPO (FOR SINGLE TOP-GAME-SORTER IMAGE):
#Rebuilding image: docker build -t gelatart/top-game-sorter:latest .
#To version: docker build -t gelatart/top-game-sorter:v2 .
#To push to registry: docker push gelatart/top-game-sorter:latest
#Pull updated image on other machine: docker pull gelatart/top-game-sorter:latest
#Run updated image on other machine: docker run -it gelatart/top-game-sorter:latest