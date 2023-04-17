from src.ml_botting_core.model_management.download_models import download_model
from loguru import logger
import json, os

def process_model_config(config):
    if 'public_models' in config:
        for config_record in config['public_models']:
            ingest_public_model(config_record)
            logger.debug(f"processed {config_record['model_name']}")
            pass
    if 'private_models' in config:
        for config_record in config['private_models']:
            ingest_private_model(config_record)
            logger.debug(f"processed {config_record['model_name']}")
            pass

def ingest_public_model(config_record):
    meta_file = f"{config_record['model_root_directory']}\\{config_record['game_state']}_meta.json"
    model_file = f"{config_record['model_root_directory']}\\{config_record['game_state']}_model.h5"
    gcp_file = f"{config_record['model_root_directory']}\\{config_record['game_state']}_gcp.json"

    locals_exists = False
    if os.path.isfile(meta_file) and os.path.isfile(model_file) and os.path.isfile(gcp_file):
        locals_exists = True

    if not locals_exists:
        # download everything and finished
        pass
    else:
        # validate latest and download if allowed
        if bool(config_record['download_latest']):
            # compare GCPs and download if needed
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
    return