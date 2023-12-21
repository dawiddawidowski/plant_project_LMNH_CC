FROM python:latest

WORKDIR /dashboard

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 8501

COPY dashboard.py .

CMD streamlit run dashboard.py