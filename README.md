## Environment setup
```
conda create --name py37-fixed python=3.7.10
conda activate py37-fixed
pip install -r req.txt
```

## Step 1: Run docker environment
```
cd aquarium/
sudo docker-compose up
```
## Step 2: Start URL feeding
- For windows
```
cd ../
./start_server_windows.bat
```
- For Linux
```
cd ../
bash ./start_server_linux.sh
```

## Step 3: Run scrapy crawler
- Change the USER_AGENT in companycrawl/settings.py to your own user agent
- Change the output_folder in companycrawl/spider/example.py to where you want to save the scraped results
```
cd companycrawl
scrapy crawl company -a http_user=user -a http_pass=userpass
```