from src.ml_botting_core import universal_predictor

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
