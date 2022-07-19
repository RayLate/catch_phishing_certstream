
import re
import math
import tqdm
import time
import os
import socket
import argparse
import time
import json
import os

pbar = tqdm.tqdm(desc='website_queue')
connection = None

if __name__ == '__main__':

    SERVER = "localhost"
    PORT = 8889
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((SERVER, PORT))
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--feed_save_path', default="D:/ruofan/phishing-kit-database/openphish/feed_download")
    parser.add_argument('--save_dir', default="D:/ruofan/New_phish30k")
    args = parser.parse_args()

    print("connected")
#     log_suspicious = "./company_list.txt"
#     with open('./brand_list.json', 'r', encoding='utf-8') as f:
#         brand_list = json.load(f)
#     print("total number of brands: {}".format(len(list(brand_list.keys()))))

    c = boto3.client(
        's3',
        aws_access_key_id="",
        aws_secret_access_key="")
    
    with open("{}/feed30day_".format(args.feed_save_path)+time_now+'.tar.gz', 'wb') as local_feed:
        c.download_fileobj('opfeeds', "premium_plus/30_days_archive.tar.gz", local_feed)
        # open file
        file = tarfile.open("{}/feed30day_".format(args.feed_save_path)+time_now+'.tar.gz')]
        os.makedirs("{}/feed30day_".format(args.feed_save_path)+time_now, exist_ok=True)
        file.extractall("{}/feed30day_".format(args.feed_save_path)+time_now)
        file.close()
        
    with open("{}/feed30day_".format(args.feed_save_path)+time_now+'/premium_phishing_feed_30_days.json', "rb") as local_feed:
        feed_today = json.load(local_feed) # print("Number of phishing {}".format(len(feed_today)))

        
    for feed in feed_today: 
        pbar.update(1)
        url = feed["url"]
        domain = clean_domain(feed["url"].split('://')[1].split('/')[0], '\/:*?"<>|')
        dirname = os.path.join(args.save_dir, domain)
        
        if os.path.exists(dirname):
            continue
        os.makedirs(dirname)
        with open(os.path.join(dirname, 'info.txt'), 'w', encoding='utf-8') as fw:
            fw.write(str(feed))
        
        try:
            connection.send(url.encode('utf-8'))
        except:
            continue



    
