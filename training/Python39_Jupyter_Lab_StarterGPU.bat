@echo off
start /min cmd /k "O: & cd O:\source\repos\ml_botting_core\training"
start /min cmd /k "O: & cd O:\source\repos\venv\Python310GPU\Scripts & activate & cd O:\source\repos\ml_botting_core\training"
start /min cmd /k "O: & cd O:\source\repos\venv\Python310GPU\Scripts & activate & cd /d O:\source\repos\ml_botting_core\training & python -m jupyter lab"