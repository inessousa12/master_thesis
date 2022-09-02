#!/bin/sh

if ! [ $(id -u) = 0 ]; then
   echo "The script need to be run as root." >&2
   exit 1
fi


#stop all containers
docker stop $(docker ps -a -q)

#remove all containers
docker rm $(docker ps -a -q)

#remove all images
docker rmi $(docker images -q)

#remove all volumes
docker volume prune -f

#clean system
docker system prune -a
