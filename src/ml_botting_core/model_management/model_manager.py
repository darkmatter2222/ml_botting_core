from src.ml_botting_core.model_management.download_models import download_model, sync_model
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
    meta_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_meta.json"
    model_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_model.h5"
    gcp_file = f"{config_record['model_root_directory']}\\{config_record['model_name']}_gcp.json"
    meta_file_exist = os.path.isfile(meta_file)
    model_file_exist = os.path.isfile(model_file)
    gcp_file_exist = os.path.isfile(gcp_file)

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
    return