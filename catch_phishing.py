
import re
import math
import tqdm
import time
import os
import socket
import argparse
import time
import json
pbar = tqdm.tqdm(desc='website_queue')
connection = None

if __name__ == '__main__':

    SERVER = "localhost"
    PORT = 8889
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connection.connect((SERVER, PORT))
    print("connected")
    log_suspicious = "./company_list.txt"

    with open('./brand_list.json', 'r', encoding='utf-8') as f:
        brand_list = json.load(f)
    print("total number of brands: {}".format(len(list(brand_list.keys()))))

    for brand in list(brand_list.keys())[int(len(list(brand_list.keys()))//3):]:
        pbar.update(1)
        domain = brand_list[brand]["url"]
        connection.send(domain.encode('utf-8'))

        if os.path.exists(log_suspicious):
            existing = set(filter(None, set(open(log_suspicious,'r').read().split('\n'))))
            with open(log_suspicious, 'a') as f:
                if domain not in existing:
                    f.write("{}\n".format(domain))
        else:
            with open(log_suspicious, 'a') as f:
                f.write("{}\n".format(domain))



    
