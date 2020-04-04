from slackbot.bot import respond_to
from attendance_slack.akashi.client import AkashiClient
from attendance_slack.akashi.dakoku_type import DakokuType


# ------出勤系-------
@respond_to(":ronrisyusya:")
def ronrisyusya(message):
    _shukkin(message)


@respond_to(":ronrishusha:")
def ronrishusha(message):
    _shukkin(message)


@respond_to(":buturishusha:")
def buturishusha(message):
    _shukkin(message)


def _shukkin(message):
    react_start(message)
    _dakoku(message, DakokuType.SHUKKIN)
    react_done(message)


# ------退勤系-------
@respond_to(":ronritaisya")
def ronritaisya(message):
    _taikin(message)


@respond_to(":ronritaisha:")
def ronritaisha(message):
    _taikin(message)


@respond_to(":buturitaisha:")
def buturitaisha(message):
    _taikin(message)


def _taikin(message):
    react_start(message)
    _dakoku(message, DakokuType.TAIKIN)
    react_done(message)


def _dakoku(message, dakoku_type):
    """
    message: slack_apiのdefaultで引き回されるmessageオブジェクト
    dakoku_type: akashi.dakoku_type.DakokuType
    """
    user_name = message._client.get_user(message.body["user"])["name"]
    AkashiClient(user_name).dakoku(dakoku_type)


def react_start(message):
    message.react('akashi')


def react_done(message):
    message.react('done')
