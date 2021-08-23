FROM ubuntu:20.04

WORKDIR /app

RUN apt-get update -y \
    && DEBIAN_FRONTEND="noninteractive" apt-get install -y \
    software-properties-common \
    vim \
    htop \
    tzdata \
    && rm -rf /var/lib/apt/lists/*

RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get install -y python3-pip python3.8 python3.8-dev libgmp3-dev

ENV TZ=American/New_York
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements* /app/requirements.txt
RUN python3.8 -m pip install pip --upgrade --force
RUN echo $PWD
RUN ls -l
RUN pip3.8 install -r requirements.txt

COPY ./entrypoint.sh /app/entrypoint.sh
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

