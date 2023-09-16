
import requests
import json
import datetime
from dotenv import load_dotenv
import os

load_dotenv()
COLLECTION = os.getenv('COLLECTION')
DATABASE = os.getenv('DATABASE')


def get_all():
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-zzctf/endpoint/data/v1/action/find"
    payload = json.dumps({
        "collection": COLLECTION,
        "database": DATABASE,
        "dataSource": "AtlasCluster",
        'filter': {}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'rBW9N6vWahvWF6fEPMQVplHf7VC9RvqsI8JDHmTnjjwKdf77c2uRtaxtcv4Vn4I8',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 200 <= response.status_code < 300:
        print(
            f'status code : {response.status_code} | document length : {len(response.json().get("documents"))}')
        return response.json().get('documents')
    print(f'status code : {response.status_code} | message : {response.text}')
    return None


def get_one(folder):
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-zzctf/endpoint/data/v1/action/findOne"
    payload = json.dumps({
        "collection": COLLECTION,
        "database": DATABASE,
        "dataSource": "AtlasCluster",
        'filter': {"folder": folder}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'rBW9N6vWahvWF6fEPMQVplHf7VC9RvqsI8JDHmTnjjwKdf77c2uRtaxtcv4Vn4I8',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 200 <= response.status_code < 300:
        print(
            f'status code : {response.status_code} | document found : {response.json().get("document")}')
        return response.json().get('document')
    print(f'status code : {response.status_code} | message : {response.text}')
    return None


def reset_collection():
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-zzctf/endpoint/data/v1/action/deleteMany"
    payload = json.dumps({
        "collection": COLLECTION,
        "database": DATABASE,
        "dataSource": "AtlasCluster",
        'filter': {}
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'rBW9N6vWahvWF6fEPMQVplHf7VC9RvqsI8JDHmTnjjwKdf77c2uRtaxtcv4Vn4I8',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 200 <= response.status_code < 300:
        print(
            f'status code : {response.status_code} | deletedCount : {response.json().get("deletedCount")}')
    else:
        print(
            f'status code : {response.status_code} | message : {response.text}')


def add_one(data: dict):
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-zzctf/endpoint/data/v1/action/insertOne"
    payload = json.dumps({
        "collection": COLLECTION,
        "database": DATABASE,
        "dataSource": "AtlasCluster",
        "document": data
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'rBW9N6vWahvWF6fEPMQVplHf7VC9RvqsI8JDHmTnjjwKdf77c2uRtaxtcv4Vn4I8',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 200 <= response.status_code < 300:
        print(
            f'status code : {response.status_code} | insertedId : {response.json().get("insertedId")}')
    else:
        print(
            f'status code : {response.status_code} | message : {response.text}')


def update_one(data: dict):
    url = "https://ap-southeast-1.aws.data.mongodb-api.com/app/data-zzctf/endpoint/data/v1/action/updateOne"
    payload = json.dumps({
        "collection": COLLECTION,
        "database": DATABASE,
        "dataSource": "AtlasCluster",
        'filter': {
            'folder': data.get('folder')
        },
        "update": data,
        'upsert': True
    })
    headers = {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': 'rBW9N6vWahvWF6fEPMQVplHf7VC9RvqsI8JDHmTnjjwKdf77c2uRtaxtcv4Vn4I8',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    if 200 <= response.status_code < 300:
        print(
            f'status code : {response.status_code} | message : {response.text}')
    else:
        print(
            f'status code : {response.status_code} | message : {response.text}')

    return response.status_code, response.text


def get_sample_data(folder='') -> dict:

    sample_data = {'folder': folder,
                   'location': '',
                   'url': '',
                   'domain': '',
                   'html_title': '',
                   'phish_prediction': 0,
                   'target_prediction': '',
                   'has_logo': False,
                   'in_target_list': False,
                   'has_forbidden_words': False,
                   'brand_inside_targetlist': False,
                   'found_knowledge': False,
                   'knowledge_discovery_branch': '',
                   'has_logo_runtime': 0,
                   'phishintention_runtime': 0,
                   'kd_runtime': 0,
                   'wi_runtime': 0,
                   'expand_targetlist_runtime': 0,
                   'total_runtime': 0,
                   'modified': None,
                   'created': int(datetime.datetime.now().timestamp())
                   }

    return sample_data
