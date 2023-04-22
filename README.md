# Welcome to ML_Botting_Core! 
**Solving Complex UI Challenges w/ ML**  
[pip install ml-botting-core](https://pypi.org/project/ml-botting-core/)  
  
![](https://img.shields.io/pypi/v/ml_botting_core?style=for-the-badge) ![](https://img.shields.io/github/actions/workflow/status/darkmatter2222/ml_botting_core/python-publish.yml?style=for-the-badge) ![](https://img.shields.io/pypi/dm/ml_botting_core?style=for-the-badge) ![TensorFlow](https://img.shields.io/badge/TensorFlow-%23FF6F00.svg?style=for-the-badge&logo=TensorFlow&logoColor=white)  ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)  
  
# Public Eve Online Models  
This package will auto download these models from [Here](https://storage.googleapis.com/eve_online_models/) at runtime and maintain a copy on your device. (and auto update)  
Sample config [Here](https://github.com/darkmatter2222/ml_botting_core/blob/main/samples/sample_config.json) with all models.

# Training
Train your own models [Here](https://github.com/darkmatter2222/ml_botting_core/blob/main/training/Universal_Classifer_Trainer.ipynb)   
Sort your training images into folders (images shape must be the same shape) and target the root for training. The classifer will train those image samples to the name of the folder they are in. 
 - Image names do not matter. 
 - PNGs only. 
 - Number of samples per folder do not matter, however you want enough, 80% for training, 20% for validation.  

├── training_data  
│   ├── char_select  
│   │   ├── image_1.png  
│   │   ├── image_2.png  
│   │   ├── image_3.png  
│   ├── connection_lost  
│   │   ├── image_1.png  
│   │   ├── image_2.png  
│   │   ├── image_3.png  
│   ├── in_flight  
│   │   ├── image_1.png  
│   │   ├── image_2.png  
│   │   ├── image_3.png  
│   ├── in_hanger  
│   │   ├── image_1.png  
│   │   ├── image_2.png  
│   │   ├── image_3.png  
  
# Usage:
Check out the samples [Here](https://github.com/darkmatter2222/ml_botting_core/tree/main/samples).  

### ml_botting_core_config.json
```json
{
   "public_models":[
      {
         "game":"eve_online",
         "model_name":"game_state",
         "download_latest":1,
         "download_latest_from":"https://storage.googleapis.com/eve_online_models/",
         "model_root_directory":"O:\\eve_live_models\\game_state",
         "model_log_directory":"O:\\eve_live_logs\\game_state",
         "save_images":0
      }
   ]
}
```


### Implementation 
```python
from ml_botting_core import universal_predictor

up_config = json.load(open(r'ml_botting_core_config.json'))
up = universal_predictor(config=up_config)

img = Image.open('some_image.png')
state_result = up.predict(img, 'game_state')
```

### state_result
```json
{
   "epoc_time":"1682138565007.508",
   "argmax_index":2,
   "value_at_argmax":"1.0",
   "class":"jump_though_first",
   "classes":[
      "dock_now",
      "invalid",
      "jump_though_first",
      "jump_through_second",
      "no_action",
      "warp_to_dock_3",
      "warp_to_dock_4"
   ],
   "scores":[
      1.2750345662162804e-15,
      1.4581948495906438e-11,
      1.0,
      5.21881417175057e-17,
      1.4712418422554443e-18,
      1.2777047215389858e-12,
      6.730089694497203e-17
   ],
   "id":"98ad373b-e0a6-11ed-9b27-2cf05d9fe8eb",
   "image_saved":0,
   "model_name":"nav_options"
}
```








