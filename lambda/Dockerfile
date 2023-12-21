FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY write_to_bucket .

CMD [ "generate_report.report_handler" ] 