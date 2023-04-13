FROM python:3.10-alpine
LABEL maintainer="admin@rhixescans.tk"
WORKDIR /core
COPY ./requirements.txt /requirements.txt
COPY . /core


RUN python -m venv /env && \
    /env/bin/pip install -r /requirements.txt && \
    adduser --disabled-password --no-create-home django-user

ENV PATH="/env/bin:$PATH"

USER django-user