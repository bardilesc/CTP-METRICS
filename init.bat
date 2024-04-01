docker-compose stop
docker-compose rm -f
docker rmi ctp-metrics
docker build -t ctp-metrics .
docker-compose up -d

