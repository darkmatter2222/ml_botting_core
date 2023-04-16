from src.ml_botting_core.universal_predictor import universal_predictor

def test_1():
    up = universal_predictor()
    assert up.load_models() == 0, "not 0"
