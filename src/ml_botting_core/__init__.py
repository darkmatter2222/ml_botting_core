import sys

try:
    sys.modules['ml_botting_core'] = sys.modules['src.ml_botting_core']
except:
    pass

from ml_botting_core.universal_predictor.universal_predictor import universal_predictor