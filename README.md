### DEV Notes

# Kill python process

netstat -apnt | grep :8000
sudo kill -9 <PID>

# run prod

## uvicorn --host 0.0.0.0 --port 8000 --reload --workers 4 app:app

# run as root

## get poetry python executable

poetry env info
/home/adm_pdf2obs/.cache/pypoetry/virtualenvs/ofml-persist-QAySIPEa-py3.12/bin/python

## start fastapi

sudo /home/adm_pdf2obs/.cache/pypoetry/virtualenvs/ofml-persist-QAySIPEa-py3.12/bin/python -m uvicorn --host 0.0.0.0 --port 8000 --reload --workers 4 app:app
