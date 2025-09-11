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