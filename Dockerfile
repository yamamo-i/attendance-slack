FROM python:3.10.7-alpine3.16

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
# 仮想環境を作成しない設定
RUN poetry config virtualenvs.create false &&  poetry install  --no-dev

ADD docker-entrypoint.sh ./
RUN chmod +x docker-entrypoint.sh
ENTRYPOINT ["./docker-entrypoint.sh"]
