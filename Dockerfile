FROM python:3.12

RUN mkdir /shop

WORKDIR /shop

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .