@echo off

start cmd /k "python server.py"
start cmd /k "python catch_phishing_certstream.py"
@REM start cmd /k "scrapy crawl company -a http_user=user -a http_pass=userpass"
