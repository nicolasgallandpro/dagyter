#!/bin/sh

if [ $# -eq 0 ]
  then
echo ""
echo "******* please choose a running container :"
docker ps --format '{{.Names}}'
echo ""
else
echo $1
docker exec -i -t $1 /bin/bash
fi
