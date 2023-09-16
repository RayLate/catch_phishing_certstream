import os
import json
import base64
from PIL import Image
from io import BytesIO
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
import requests

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
import requests

class CaptchaIdentifier:

    def __init__(self):
        self.DOCKER_HOSTNAME = "192.168.59.130"
        self.PORT = "5000"
        self.URL = f'http://{self.DOCKER_HOSTNAME}:{self.PORT}'

    def reset_database(self):
        res = requests.post(f'{self.URL}/database/reset')
        print(f'status code <{res.status_code}>')
        if res.status_code == 200:
            print('databased reset successfully')
        else:
            print('something went wrong')

    def make_prediction(self, screenshot: str):
        # screenshot in base 64
        payload = {'screenshot': screenshot}
        headers = {"Content-Type": "application/json; charset=utf-8"}
        # print(f'payload: {json.dumps(payload)}')
        res = requests.post(f'{self.URL}/predict', json=payload, headers=headers)
        print(f'status code <{res.status_code}>')
        print(res.json())
        if res.status_code == 200:
            return res.json()


def get_ip_location(domain):
    import requests
    import json
    from iplookup import iplookup

    ip = iplookup.iplookup

    # IP address to test
    ip_address = ip(domain)
    if ip_address:
        ip_address = ip_address[0]
        request_url = 'https://geolocation-db.com/jsonp/' + ip_address
        response = requests.get(request_url)
        result = response.content.decode()
        result = result.split("(")[1].strip(")")
        result = json.loads(result)
        return result.get('country_name')
    return ''


def convert_image_to_base64(path: str) -> str:
    # Set the path to your image file
    image_path = path

    try:
        # Check if the file exists and is a valid image file
        if not os.path.exists(image_path):
            raise ValueError("File not found")

        if not Image.open(image_path).format:
            raise ValueError("File is not a valid image")

        # Open the image file using PIL
        with open(image_path, 'rb') as image_file:
            image = Image.open(image_file)

            # Convert the image to a base64 string
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Print the base64 string
            return img_str

    except Exception as e:
        print(f"Error: {str(e)}")


def append(path: str, message: str):
    with open(path, 'a') as f:
        f.write(message + '\n')


def check_duplicate(path: str, website: str):
    with open(path, 'r') as f:
        body = f.read()
        if website in body:
            return True
        return False


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
        output_folder = "E://screenshots_rf/{}".format(datetime.today().strftime('%Y-%m-%d'))
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
                # time.sleep(0.1)
                url = 'https://' + msg
                domain = self.clean_domain(url, '\/:*?"<>|')
                if os.path.exists(os.path.join(self.get_output_folder(), domain, 'html.txt')):
                    # check domain in output folder, if present, skip
                    continue

                splash_args = {
                    'lua_source': script,
                    'filters': 'fanboy-annoyance',
                    'timeout': 15,
                    'resource_timeout': 15,
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
        if len(os.listdir(self.get_output_folder())) >= 100: # daily crawling limit
            return
        print(f'crawled page {domain}...')
        output_folder = os.path.join(self.get_output_folder(), domain)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        screenshot_path = os.path.join(output_folder, "shot.png")
        info_path = os.path.join(output_folder, "info.txt")
        html_path = os.path.join(output_folder, "html.txt")

        with open('url_success_crawled.txt', 'a') as f:
            timestamp = datetime.now().strftime('%m-%d %H:%M:%S')
            log_message = f'[{timestamp}] {str(domain)}'
            f.write(log_message + '\n')

        with open(screenshot_path, 'wb+') as f:
            f.write(png_bytes)

        with open(info_path, 'w+') as f:
            f.write(response.data['url'])

        with open(html_path, 'wb+') as f:
            f.write(response.body)

        #get domain location
        location = ''
        detected = ''
        results = ''
        try:
            location = get_ip_location(domain)
        except Exception as e:
            pass

        # Captcha Detection
        result_path = r'C:\Users\Ruofan\PycharmProjects\MyScrapy\companycrawl\companycrawl\result.txt'
        # base64_img = convert_image_to_base64(screenshot_path)
        # if not base64_img or check_duplicate(result_path, domain):
        #     return
        # result = CaptchaIdentifier().make_prediction(base64_img)
        # detected = result.get('detected', False)
        # results = result.get('results', [])
        message = f'{domain};{detected};{results};{location}'
        append(result_path, message)
        # if detected:
        #     print(domain, 'contains Captcha')

        # Run Dynaphish
        isDynaphishUp = False
        try:
            response = requests.get('http://192.168.59.130:5002')
            if response.status_code >= 200 and response.status_code < 300:
                isDynaphishUp = True
        except requests.RequestException as e:
            print("Error connecting to Dynaphish Server")
            isDynaphishUp = False

        if isDynaphishUp:
            folder_path = '/mnt/hgfs/screenshots_rf/{}/{}'.format(datetime.today().strftime('%Y-%m-%d'),domain)
            requests.get(f'http://192.168.59.130:5002/task?folder_path={folder_path}')

        # To run the Crawler
        # scrapy crawl company -a http_user=user -a http_pass=userpass

    def url_join(self, urls, response):
        joined_urls = []
        for url in urls:
            joined_urls.append(response.urljoin(url))

        return joined_urls
