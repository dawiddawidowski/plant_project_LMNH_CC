FROM python:latest

WORKDIR /usr/src/app

COPY requirements.txt .
COPY multi_extract.py .
COPY transform_readings.py .
COPY load.py .
COPY pipeline.py .

RUN pip install -r requirements.txt

CMD python3 pipeline.py