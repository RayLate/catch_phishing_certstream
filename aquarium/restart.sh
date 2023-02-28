cd ~/aquarium/
sudo service docker restart
while true
do
    sleep 5
    sudo docker-compose up -d
    sleep 180
    sudo kill -s SIGINT $(sudo docker ps -a -q)
    sudo service docker restart
done