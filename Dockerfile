FROM python:3.7.7-alpine3.11

RUN apk update \
        && apk add --no-cache git openssh-client \
        && pip install pipenv

RUN mkdir -p /app/src
WORKDIR /app/src
ADD *.py ./
ADD attendance_slack ./attendance_slack
ADD Pipfile* ./
RUN pipenv install --python /usr/local/bin/python

ENTRYPOINT ["pipenv", "run", "python", "run.py"]
