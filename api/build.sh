docker login
docker build -t dbuckleysm/docker-fastapi -f ./production/Dockerfile . --no-cache
docker push dbuckleysm/docker-fastapi