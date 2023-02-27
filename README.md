## Summary
In this repository, I implement a customized scrapy crawler to crawl a list of URLs with its HTML, screenshot, information.

## Environment setup [! We find that the scrapy crawler only works with python version 3.7.10]
```
conda create --name py37-fixed python=3.7.10
conda activate py37-fixed
pip install -r req.txt
```

## Step 1: Run docker environment
As long as the docker is turn on, the docker environment starts automatically every hour starting from 00:00 am
To check if the docker is running proper, on firefox go to `0.0.0.0:8036`. if the page does not load run the code below
```
cd aquarium/
sudo docker-compose up
```
Note that if you are using Windows, you need a virtual machine with [Ubuntu image](https://techloudgeek.com/download/image/?link=https://dlhzub60.linuxvmimages.com/) to run this step. 
- You need to configure [NAT port forwarding](https://www.virten.net/2013/03/how-to-setup-port-forwarding-in-vmware-workstation-9/) in order to connect VM to network.
- Then move the aquarium folder into the VM, [install docker on VM](https://docs.docker.com/engine/install/ubuntu/).
- Run the two commands in terminal
- Change the SPLASH_URL = 'http://[ip address of your VM]:8050' in companycrawl/settings.py 
- Only step1 needs an ubuntu machine, step2 and step3 can be run locally.

## Step 2: Start URL feeding, feed obtained from Certstream
- For windows
```
cd ../
start_server_windows_certstream.bat
```
- For Linux
```
cd ../
bash ./start_server_linux_certstream.sh
```
## Step 3: Run scrapy crawler
- Change the USER_AGENT in companycrawl/settings.py to your own user agent
- Change the output_folder in companycrawl/spider/example.py to where you want to save the scraped results
```
cd companycrawl
scrapy crawl company -a http_user=user -a http_pass=userpass
```