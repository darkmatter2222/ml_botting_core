# Imports
from src.ml_botting_core import universal_predictor
import json
from PIL import Image

# Load in Configuration
up_config = json.load(open(r'sample_config.json'))

# Initialize
up = universal_predictor(config=up_config)

# Load in image or Screen Grab
img = Image.open('sample_nav_options_jump_through_first.png')

# Render prediction from model w/ image as input.
state_result = up.predict(img, 'nav_options')

print(state_result)



