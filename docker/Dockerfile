FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/BotWebo2/

RUN apt update \
    && apt install -y --no-install-recommends make cmake python python3-pip ffmpeg
    
COPY . /BotWebo2

WORKDIR /BotWebo2

RUN python3 -m pip install -U pip
    && pip install -r requirements.txt  \
    && chmod +x ./docker/startContainer.sh \
    && chmod +x ./sources/main.py

ENTRYPOINT ["./docker/startContainer.sh"]
