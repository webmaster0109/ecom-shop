FROM python:3.10.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

WORKDIR /ecom_app

COPY requirements.txt /ecom_app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /ecom_app/
