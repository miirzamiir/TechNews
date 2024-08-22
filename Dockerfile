FROM python:3.11

ENV PYTHONUNBUFFERED=1

RUN groupadd -g 1000 techuser && useradd -u 1000 -g techuser -m techuser

WORKDIR /app

RUN apt-get update
RUN apt-get install -y wget
RUN wget -q https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt-get install -y ./google-chrome-stable_current_amd64.deb

COPY ./requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

RUN chown -R techuser:techuser /app
USER techuser

EXPOSE 8000