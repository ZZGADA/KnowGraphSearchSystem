

FROM ubuntu:20.04
RUN sed -i 's@http://archive.ubuntu.com/ubuntu/@http://mirrors.aliyun.com/ubuntu/@g' /etc/apt/sources.list
RUN apt-get update -y &&\
    apt-get -y install iputils-ping \
    && apt-get -y install wget \
    && apt-get -y install net-tools \
    && apt-get -y install vim \
    && apt-get -y install openssh-server \
    && apt-get -y install python3.9 \
    && apt-get -y install python3-pip python3-dev \
    && cd /usr/local/bin \
    && rm -f python \
    && rm -f python3 \
    && rm -f pip \
    && rm -f pip3 \
    && ln -s /usr/bin/python3.9 python \
    && ln -s /usr/bin/python3.9 python3 \
    && ln -s /usr/bin/pip3 pip \
    && ln -s /usr/bin/pip3 pip3 \
    && python -m pip install --upgrade pip \
    && apt-get clean \
    && rm -rf /tmp/* /var/lib/apt/lists/* /var/tmp/* \
ENV LANG C.UTF-8
WORKDIR /zstp
COPY . /zstp
RUN pip  --no-cache-dir install -r  requirements.txt -i https://pypi.mirrors.ustc.edu.cn/simple/
EXPOSE 28081


