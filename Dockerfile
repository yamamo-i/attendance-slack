FROM python:3.9.11-alpine3.15

RUN apk update \
    && apk add --no-cache git openssh-client build-base musl-dev libffi-dev \
    && pip install poetry

RUN mkdir -p /app/src
WORKDIR /app/src
ADD *.py ./
ADD attendance_slack ./attendance_slack
ADD poetry.lock ./
ADD pyproject.toml ./
ADD bin ./bin
RUN poetry install

ADD docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
