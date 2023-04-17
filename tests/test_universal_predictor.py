from src.ml_botting_core.universal_predictor import universal_predictor
import json


def test_singleton():
    config = {}
    up1 = universal_predictor(config=config)
    up1.regressors['test'] = 1
    up2 = universal_predictor(config=config)
    assert up1.regressors['test'] == up2.regressors['test'], 'universal_predictor not singleton'


def test_missing_config():
    try:
        universal_predictor()
    except Exception as e:
        assert e == Exception("universal_predictor missing configuration"), "unexpected exception"


def test_download_model():
    config = json.loads(open("tests\\test_model_config.json").read())
    up = universal_predictor(config=config)
    up.load_models()
