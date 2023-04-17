from src.ml_botting_core.model_management.download_models import download_model
from loguru import logger
import json

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
    try:
        f = open(f"{config_record['model_root_directory']}\\{config_record['game_state']}_meta.json", "r")
        installed_models = json.loads(f.read())
        f.close()
    except:
        #logger.info('installed_models file missing, proceeding w/ new.')
        pass
    return

def ingest_private_model(config_record):
    return