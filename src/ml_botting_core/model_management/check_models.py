import requests, xmltodict
def check_model(config_record):
    if bool(config_record['download_latest']):
        r = requests.get(config_record['download_source_root'], allow_redirects=True)
        data_dict = xmltodict.parse(r.content)
        available_models = {}
        pass
    else:

    return