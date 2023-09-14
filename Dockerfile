FROM python:3.8

RUN mkdir /sdu_tt

WORKDIR /sdu_tt

COPY . .

RUN python -m pip install --upgrade pip && \
    pip install -r requirements.txt