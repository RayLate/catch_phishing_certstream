import os
import json
import base64
import scrapy
from scrapy_splash import SplashRequest
import pandas as pd
from urllib.parse import urlparse
import os
import socket
import websockets
import time
import json

script = """
function main(splash, args)
  splash:set_viewport_size(1920,1080)
  assert(splash:go(splash.args.url))
  assert(splash:wait(3))
  return {
    html = splash:html(),
    png = splash:png(),
    har = splash:har(),
    url = splash:url()
  }
end
"""

class MyItem(scrapy.Item):
    # ... other item fields ...
    image_urls = scrapy.Field()
    images = scrapy.Field()
    file_path = scrapy.Field()


class ExtractSpider(scrapy.Spider):
    name = 'company'
    num = 0

    custom_settings = {
        "HTTPERROR_ALLOWED_CODES": [503],
    }

    def clean_domain(self, domain, deletechars='\/:*?"<>|'):
        for c in deletechars:
            domain = domain.replace(c, '')
        return domain

    def start_requests(self):

        SERVER = "localhost"
        PORT = 8889
        print("start")
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((SERVER, PORT))
        print("connected")

        while True:
            if self.num > 100:
                print(self.num)
                time.sleep(5)
                self.num -= 10
            connection.send('1'.encode('utf-8'))
            msg = connection.recv(2048)
            msg = msg.decode('utf-8')
            if msg == '1':
                time.sleep(1)
                continue
            else:
                url = msg
                if '*.' in url:
                    continue
                url = 'https://' + url
                output_folder = "/home/ruofan/git_space/company" # FIXME: to change
                domain = self.clean_domain(url, '\/:*?"<>|')
                if os.path.exists(os.path.join(output_folder, domain, 'html.txt')):
                    continue

                splash_args = {
                    'lua_source': script,
                    'filters': 'fanboy-annoyance',
                    'timeout': 10,
                    'resource_timeout': 10
                }

                yield SplashRequest(url, self.parse_result, endpoint='execute', args=splash_args)

    def parse_result(self, response):

        if response.status == 503:
            print(self.num)
            self.num += 1
            return
        else:
            self.num -= 1
            self.num = max(0, self.num)

        domain = self.clean_domain(urlparse(response.data['url']).netloc, '\/:*?"<>|')

        png_bytes = base64.b64decode(response.data['png'])

        output_folder = "/home/ruofan/git_space/company" # FIXME: to change
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        output_folder = os.path.join(output_folder, domain)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        screenshot_path = os.path.join(output_folder, "shot.png")
        info_path = os.path.join(output_folder, "info.txt")
        html_path = os.path.join(output_folder, "html.txt")

        with open(screenshot_path, 'wb+') as f:
            f.write(png_bytes)

        with open(info_path, 'w+') as f:
            f.write(response.data['url'])

        with open(html_path, 'wb+') as f:
            f.write(response.body)

    def url_join(self, urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))

        return joined_urls
