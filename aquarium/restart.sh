#!/bin/sh
cd /home/qing/aquarium

for index in 0 1 2 3 4
do 
	sudo docker-compose restart splash$index
done
