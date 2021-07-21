FROM ubuntu:20.04

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONPATH=/BotWebo2/

COPY . /BotWebo2
WORKDIR /BotWebo2

RUN apt update \
    && apt install -y --no-install-recommends python python3-pip ffmpeg libsodium-dev libffi-dev python3-dev build-essential \
    && python3 -m pip install -U pip \
    && SODIUM_INSTALL=system pip install pynacl \
    && pip install -r requirements.txt  \
    && chmod +x ./docker/startContainer.sh \
    && python3 ./docker/InstallCertificates.command \
    && apt remove -y libffi-dev python3-dev build-essential \
    && apt autoremove -y \
    && chmod +x ./sources/main.py

ENTRYPOINT ["./docker/startContainer.sh"]