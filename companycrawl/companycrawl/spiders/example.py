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
from datetime import datetime
from PIL import Image
import cv2
import numpy as np
import io

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

    def get_output_folder(self):
        output_folder = "D://{}".format(datetime.today().strftime('%Y-%m-%d'))
        return output_folder

    def clean_domain(self, domain, deletechars='\/:*?"<>|'):
        for c in deletechars:
            domain = domain.replace(c, '')
        return domain

    @staticmethod
    def white_screen(old_screenshot_img):
        old_screenshot_img = old_screenshot_img.convert("RGB")
        old_screenshot_img_arr = np.asarray(old_screenshot_img)
        old_screenshot_img_arr = np.flip(old_screenshot_img_arr, -1)  # RGB2BGR
        img = cv2.cvtColor(old_screenshot_img_arr, cv2.COLOR_BGR2GRAY)

        img_area = np.prod(img.shape)
        white_area = np.sum(img == 255)
        if white_area / img_area >= 0.9:  # skip white screenshots
            return True  # dirty
        return False

    def start_requests(self):

        SERVER = "localhost"
        PORT = 8889
        print("start")
        connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        connection.connect((SERVER, PORT))
        print("connected")

        while True:
            if self.num > 100:
                # after 100 503 error, rest for 5 second, this prevents server overloading
                print(self.num)
                time.sleep(5)
                self.num -= 10
            connection.send('1'.encode('utf-8'))
            msg = connection.recv(2048)
            msg = msg.decode('utf-8')
            if msg == '1':
                # if the return message is '1', means the queue is empty
                # wait and try again
                time.sleep(1)
                continue
            else:
                # else an url is returned
                url = msg
                if '*.' in url:
                    continue
                url = 'https://' + url

                domain = self.clean_domain(url, '\/:*?"<>|')
                if os.path.exists(os.path.join(self.get_output_folder(), domain, 'html.txt')):
                    # check domain in output folder, if present, skip
                    continue

                splash_args = {
                    'lua_source': script,
                    'filters': 'fanboy-annoyance',
                    'timeout': 20,
                    'resource_timeout': 20
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
        screenshot_img = Image.open(io.BytesIO(png_bytes))
        if self.white_screen(screenshot_img):
            return

        if not os.path.exists(self.get_output_folder()):
            os.makedirs(self.get_output_folder())
        if len(os.listdir(self.get_output_folder())) >= 3000: # daily crawling limit
            return

        output_folder = os.path.join(self.get_output_folder(), domain)
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
