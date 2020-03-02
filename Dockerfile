FROM python:3.8-slim
MAINTAINER Kevin Coakley <kcoakley@sdsc.edu>

ADD . /tmp/install
WORKDIR /tmp/install

RUN pip install -r requirements.txt
RUN ./setup.py install

RUN groupadd -g 999 swift && \
    useradd -r -u 999 -g swift swift

USER swift

CMD swift-archive --debug