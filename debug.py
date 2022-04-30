import json
from urllib.parse import urlparse
import os
import shutil
import tqdm

def clean_domain(domain, deletechars='\/:*?"<>|'):
    for c in deletechars:
        domain = domain.replace(c, '')
    return domain

if __name__ == '__main__':
    # with open('./brand_list.json', 'r', encoding='utf-8') as f:
    #     brand_list = json.load(f)
    # print("total number of brands: {}".format(len(list(brand_list.keys()))))
    #
    # domains = [brand_list[brand]["url"] for brand in list(brand_list.keys())[int(len(list(brand_list.keys()))//3):int(len(list(brand_list.keys()))//3)*2]]
    # print("total number of interested domains {}".format(len(domains)))
    # print(domains[:10])
    # ct = 0
    # for folder in tqdm.tqdm(os.listdir("/home/ruofan/git_space/company")):
    #     if folder.replace('www.', '') not in domains:
    #         ct += 1
    #         # if len(folder) > 0:
    #             # shutil.rmtree(os.path.join("/home/ruofan/git_space/company", folder))
    #
    # print(ct)

    # with open("crawled_companies.txt", 'a+') as f:
    #     for folder in tqdm.tqdm(os.listdir("/home/ruofan/git_space/company")):
    #         f.write(folder+'\n')

    ct = 0
    for folder in tqdm.tqdm(os.listdir("/home/ruofan/git_space/company")):
        if folder in open("crawled_companies_125.txt", encoding='utf-8').read():
            ct += 1
            if not os.path.isdir(os.path.join("/home/ruofan/git_space/company", folder)):
                continue
            shutil.rmtree(os.path.join("/home/ruofan/git_space/company", folder))
    print(ct)


