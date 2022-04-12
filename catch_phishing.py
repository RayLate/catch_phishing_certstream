
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
import signal
from subprocess import Popen, PIPE

pbar = tqdm.tqdm(desc='website_queue')
connection = None

if __name__ == '__main__':

    SERVER = "localhost"
    PORT = 8889
    connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        connection.connect((SERVER, PORT))
    except OSError:
        process = Popen(["sudo lsof", "-i", ":{0}".format(PORT)], stdout=PIPE, stderr=PIPE)
        stdout, stderr = process.communicate()
        for process in str(stdout.decode("utf-8")).split("\n")[1:]:
            data = [x for x in process.split(" ") if x != '']
            if (len(data) <= 1):
                continue
            os.kill(int(data[1]), signal.SIGKILL)

    print("connected")
    log_suspicious = "./company_list.txt"

    with open('./brand_list.json', 'r', encoding='utf-8') as f:
        brand_list = json.load(f)
    print("total number of brands: {}".format(len(list(brand_list.keys()))))

    for brand in list(brand_list.keys())[int(len(list(brand_list.keys()))//3):int(len(list(brand_list.keys()))//3)*2]: # FIXME: replace with your own URL list
        pbar.update(1)
        domain = brand_list[brand]["url"]
        try:
            connection.send(domain.encode('utf-8'))

            if os.path.exists(log_suspicious):
                existing = set(filter(None, set(open(log_suspicious,'r').read().split('\n'))))
                with open(log_suspicious, 'a') as f:
                    if domain not in existing:
                        f.write("{}\n".format(domain))
            else:
                with open(log_suspicious, 'a') as f:
                    f.write("{}\n".format(domain))
        except:
            continue



    
