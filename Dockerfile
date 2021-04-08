FROM python:3.8-slim-buster
ENV PYTHONUNBUFFERED=1

RUN python -m pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
RUN python -m nltk.downloader punkt averaged_perceptron_tagger

COPY ./app ./app

# Local Only!!!
COPY .env .env
# end

EXPOSE 8000
CMD uvicorn app.main:app --host 0.0.0.0 --port 8000
