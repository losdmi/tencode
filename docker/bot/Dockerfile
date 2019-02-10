FROM ubuntu:18.04

LABEL maintainer="dimaconway@gmail.com"

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update \
    && apt-get install -y gnupg tzdata \
    && echo 'UTC' > /etc/timezone \
    && dpkg-reconfigure -f noninteractive tzdata

#RUN apt-get update \
#    && apt-get install -y cron curl zip unzip git \
#       software-properties-common \
#    && add-apt-repository -y ppa:ondrej/php \
#    && apt-get update \
#    && apt-get install -y php7.2-cli php7.2-zip php7.2-mbstring \
#       php7.2-xml php7.2-curl \
#    && mkdir /app \
#    && apt-get remove -y --purge software-properties-common \
#    && apt-get -y autoremove \
#    && apt-get clean \
#    && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

# Create the log file to be able to run tail
#RUN touch /var/log/cron.log


ARG src
ARG app_root
COPY ${src} ${app_root}


WORKDIR ${app_root}
#ENTRYPOINT ./entrypoint.sh
