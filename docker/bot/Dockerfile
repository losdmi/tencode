FROM ubuntu:18.04

LABEL maintainer="dimaconway@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

ARG src
ARG app_root

WORKDIR ${app_root}

RUN apt-get update \
    && apt-get install -y gnupg tzdata \
    && echo 'UTC' > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

RUN apt-get update \
    && apt-get install -y curl \
#       zip unzip git \
       software-properties-common \
    && add-apt-repository -y ppa:deadsnakes/ppa \
    && apt-get install -y python3.7 python3-pip\
    && apt-get remove -y --purge software-properties-common \
    && apt-get -y autoremove \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* \
    && ln -s /usr/bin/python3.7 /usr/bin/python \
    && python -m pip install --upgrade pip


# Create the log file to be able to run tail
#RUN touch /var/log/cron.log


ENV WORKON_HOME=${app_root}/.venvs
ENV PIPENV_VENV_IN_PROJECT=1
COPY ${src}/* ${app_root}/
RUN python -m pip install -r requirements.txt

ENTRYPOINT python bot.py
