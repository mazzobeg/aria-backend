## Build the projet
Construct a dev environnement using venv.
```
python -m venv env
```
Install dependancies
```
pip install -r requirements.txt
```
Update dependancies
```
pip freeze > requirements.txt
```
Run the flask application
```
python run.py
```
Run tests (deprecated)
```
python -m unittest discover tests
```
Run tests
```
pytest
```