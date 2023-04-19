# Welcome to ML_Botting_Core! 
**Solving Complex UI Challenges w/ ML**  
[pip install ml-botting-core](https://pypi.org/project/ml-botting-core/)  
  
![](https://img.shields.io/pypi/v/ml_botting_core?style=for-the-badge) ![](https://img.shields.io/github/actions/workflow/status/darkmatter2222/ml_botting_core/python-publish.yml?style=for-the-badge) ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
  
# Public Eve Online Models  
This package will auto download these models from [Here](https://storage.googleapis.com/eve_online_models/) at runtime and maintain a copy on your device. (and auto update)
  
# Usage:
### ml_botting_core_config.json
```json
{
   "public_models":[
      {
         "game":"eve_online",
         "model_name":"game_state",
         "download_latest":1,
         "download_latest_from":"https://storage.googleapis.com/eve_online_models/",
         "model_root_directory":"O:\\eve_live_models\\game_state"
      }
   ]
}
```


### Implementation 
```python
from ml_botting_core import universal_predictor

up_config = json.load(open(r'ml_botting_core_config.json'))
up = universal_predictor(config=up_config)
up.load_models()

img = Image.open('some_image.png')
state_result = up.predict(img, 'game_state')
```

### state_result
```json
{
   "argmax_index":0,
   "value_at_argmax":0.76277816,
   "class":"char_select",
   "classes":[
      "char_select",
      "connection_lost",
      "in_flight",
      "in_hanger"
   ],
   "scores":[
      0.7627781629562378,
      0.004260888323187828,
      3.3299270398856606e-06,
      0.23295757174491882
   ],
   "id": UUID("57a29474-de52-11ed-a215-2cf05d9fe8eb"),
   "image_saved":0,
   "model_name":"game_state"
}
```








