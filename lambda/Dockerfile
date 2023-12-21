FROM public.ecr.aws/lambda/python:latest

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY upload_old_data.py .

CMD [ "upload_old_data.lambda_handler" ] 