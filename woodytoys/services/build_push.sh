#/bin/bash

set -e

default_version="3"
version=${1:-"$default_version"}


docker build -t correba/woody_api:"$version" api 
docker tag correba/woody_api:"$version" correba/woody_api:latest

docker build -t correba/woody_rp:"$version" reverse-proxy
docker tag correba/woody_rp:"$version" correba/woody_rp:latest

docker build -t correba/woody_database:"$version" database
docker tag correba/woody_database:"$version" correba/woody_database:latest

docker build -t correba/woody_front:"$version" front
docker tag correba/woody_front:"$version" correba/woody_front:latest


# avec le "set -e" du début, je suis assuré que rien ne sera pushé si un seul build ne c'est pas bien passé

docker push correba/woody_api:"$version"
docker push correba/woody_api:latest

docker push correba/woody_rp:"$version"
docker push correba/woody_rp:latest

docker push correba/woody_front:"$version"
docker push correba/woody_front:latest

docker push correba/woody_database:"$version"
docker push correba/woody_database:latest
