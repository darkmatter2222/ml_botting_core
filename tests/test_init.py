from src.ml_botting_core.universal_predictor import universal_predictor

up = universal_predictor()

assert up.load_models() == '', "should be blank"