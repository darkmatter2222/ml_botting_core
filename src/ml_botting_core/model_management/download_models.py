import errno
import json
import os
import requests
import xmltodict
from loguru import logger


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def get_gcp_config(config_record):
    r = requests.get(config_record['download_latest_from'], allow_redirects=True)
    data_dict = xmltodict.parse(r.content)
    available_models = {}
    for obj in data_dict['ListBucketResult']['Contents']:
        key_split = obj['Key'].split('/')
        if config_record['model_name'] == key_split[0]:
            available_models[key_split[0]] = available_models[key_split[0]] if key_split[0] in available_models else {}
            available_models[key_split[0]][key_split[1]] = obj

    logger.info(f"GCP Downloaded for {config_record['model_name']}, {len(available_models.keys())} records found")

    if len(available_models.keys()) == 0:
        raise Exception("No Models Configured for Download")

    return available_models


def load_installed_model(config_record):
    f = open(f"{config_record['model_root_directory']}\\{config_record['model_name']}_gcp.json", "r")
    installed_models = json.loads(f.read())
    f.close()
    return installed_models


def sync_model(config_record):
    available_models = get_gcp_config(config_record)
    installed_models = load_installed_model(config_record)
    if installed_models[config_record['model_name']] != available_models[config_record['model_name']]:
        logger.info(f"Update available, downloading...")
        download_model(config_record, available_models)
    else:
        logger.info(f"Models up to date")


def download_model(config_record, available_models=None):
    if available_models == None:
        available_models = get_gcp_config(config_record)

    for file_key in available_models[config_record['model_name']]:
        logger.info(f"Downloading {config_record['model_root_directory']}\\{file_key}")
        outfile = f"{config_record['model_root_directory']}\\{file_key}"
        mkdir_p(config_record['model_root_directory'])
        upfile = f"{config_record['download_latest_from']}{available_models[config_record['model_name']][file_key]['Key']}"
        r = requests.get(upfile, allow_redirects=True, stream=True)
        open(outfile, 'wb').write(r.content)

    logger.info(f"Downloading {config_record['model_name']}_gcp.json")
    outfile = f"{config_record['model_root_directory']}\\{config_record['model_name']}_gcp.json"
    open(outfile, 'w').write(json.dumps(available_models, indent=1))

    logger.info(f"Download complete")
