FROM python:3.12.2

# container folder
WORKDIR /app

COPY pyproject.toml pyproject.toml
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# make ebase builder executable
RUN chmod +x ./tools/linux/ebmkdb && chmod +x ./run.sh

EXPOSE 8000

#CMD gunicorn --bind 0.0.0.0:9000 --timeout 600 --workers 2 --threads 2 wsgi:app
CMD  python -m uvicorn --host 0.0.0.0 --port 8000  --workers 4 app:app