import json
import os
import errno

import tensorflow as tf
from loguru import logger

from .download_models import download_model, sync_model


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def construct_dirs(config_record):
    if not os.path.isdir(config_record['model_root_directory']):
        mkdir_p(config_record['model_root_directory'])

    if not os.path.isdir(config_record['model_log_directory']):
        mkdir_p(config_record['model_log_directory'])


def get_local_file_locations(config_record):
    meta_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_meta.json"
    model_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_model.h5"
    gcp_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_gcp.json"

    meta_file_exist = os.path.isfile(meta_file)
    model_file_exist = os.path.isfile(model_file)
    gcp_file_exist = os.path.isfile(gcp_file)

    return meta_file, model_file, gcp_file, meta_file_exist, model_file_exist, gcp_file_exist


def process_model_config(config):
    if 'public_models' in config:
        for config_record in config['public_models']:
            construct_dirs(config_record)
            ingest_public_model(config_record)
            logger.info(f"PreProcessed public_models {config_record['model_name']}")
            pass
    # TODO, Build This
    if 'private_models' in config:
        for config_record in config['private_models']:
            ingest_private_model(config_record)
            logger.info(f"PreProcessed private_models {config_record['model_name']}")
            pass


def load_models_from_config(config):
    process_model_config(config)
    classifiers = {}
    if 'public_models' in config:
        for config_record in config['public_models']:
            classifiers[config_record['model_name']] = load_model(config_record)
            logger.info(f"Loaded {config_record['model_name']}")
            pass
    # TODO, Build This
    if 'private_models' in config:
        for config_record in config['private_models']:
            pass
    return classifiers


def load_model(config_record):
    meta_file, model_file, gcp_file, meta_file_exist, model_file_exist, gcp_file_exist = get_local_file_locations(
        config_record)
    # TODO, make thi agnostic to model type

    if not meta_file_exist or not model_file_exist or not gcp_file_exist:
        error = 'Attempted to load models that are not downloaded'
        logger.error(error)
        raise Exception(error)

    classifier = {
        'config_record': config_record,
        'model': tf.keras.models.load_model(model_file),
        'meta': json.loads(open(meta_file, 'r').read()),
        'gcp': json.loads(open(gcp_file, 'r').read()),
    }

    return classifier


def ingest_public_model(config_record):
    meta_file, model_file, gcp_file, meta_file_exist, model_file_exist, gcp_file_exist = get_local_file_locations(
        config_record)

    locals_exists = False
    if meta_file_exist and model_file_exist and gcp_file_exist:
        locals_exists = True

    if not locals_exists:
        if bool(config_record['download_latest']):
            # Download Latest regardless of existence
            download_model(config_record)
            pass
        else:
            # No model exists and we cant download? but we are asking to run this model?
            error = f"{config_record['model_name']} does not completely exist, not permitted to download fresh copy."
            error += f" - Meta file exists at '{meta_file}':{meta_file_exist}"
            error += f" - Model file exists at '{model_file}':{model_file_exist}"
            error += f" - GCP file exists at '{gcp_file}':{gcp_file_exist}"
            logger.error(error)
            raise Exception(error)
        # download everything and finished
        pass
    else:
        # validate latest and download if allowed
        if bool(config_record['download_latest']):
            # compare GCPs and download if needed
            sync_model(config_record)
            pass
        else:
            # do nothing, we are done
            pass

    try:

        f = open(meta_file, "r")
        installed_models = json.loads(f.read())
        f.close()
    except:
        logger.info('installed_models file missing, proceeding w/ new.')
        pass
    return


def ingest_private_model(config_record):
    # TODO, Build this
    return
