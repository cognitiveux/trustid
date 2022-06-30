# TRUSTID
TRUSTID backend


# Local development

# Create docker network if it doesn't exist
docker network create trustid-network

# Build the docker image
docker-compose build --no-cache

# Start the containers
docker-compose up

# Links
- Documentation: http://localhost:10000/backend/doc/
- Interactive Demo: http://localhost:10000/backend/demo/
