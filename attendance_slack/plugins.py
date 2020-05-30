from slackbot.bot import respond_to
from attendance_slack.akashi.dakoku_type import DakokuType
from attendance_slack.akashi.exception import BadShukkinStateException, BadTaikinStateException, UserNotFoundException
from attendance_slack.akashi.use_case import AkashiUseCase


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


@respond_to(":rimowakaishi:")
def rimowakaishi(message):
    _shukkin(message)


def _shukkin(message):
    _dakoku(message, DakokuType.SHUKKIN)


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


@respond_to(":rimowashuryo:")
def rimowashuryo(message):
    _taikin(message)


def _taikin(message):
    _dakoku(message, DakokuType.TAIKIN)


def _dakoku(message, dakoku_type):
    """
    message: slack_apiのdefaultで引き回されるmessageオブジェクト
    dakoku_type: akashi.dakoku_type.DakokuType
    """
    message.react('akashi')
    try:
        user_name = message._client.get_user(message.body["user"])["name"]
        AkashiUseCase.dakoku(user_name, dakoku_type)
    except UserNotFoundException:
        message.reply("ぜひ管理者にユーザ登録してもらってね :hugging_face:")
    except BadShukkinStateException:
        message.reply("前営業日の退勤の打刻をしていないかも :thinking_face:")
    except BadTaikinStateException:
        message.reply("出勤の打刻をしていないかも :thinking_face:")
    except Exception as e:
        message.reply("技術的な問題で打刻できませんでした :cry: 管理者が解析します :pray:")
        message.react('damedatta')
        raise e
    else:
        message.react('done')
