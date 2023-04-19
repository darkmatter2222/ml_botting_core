from src.ml_botting_core import universal_predictor
from PIL import Image
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

def test_prediction():
    model_name = 'game_state'
    img = Image.open('tests\\test_images\\set_dest_second_pos_test.png')
    config = json.loads(open('tests\\test_model_configs\\test_model_config.json', 'r').read())
    up = universal_predictor(config=config)
    up.load_models()
    result = up.predict(img, model_name)
    assert result['model_name'] == model_name

test_prediction()