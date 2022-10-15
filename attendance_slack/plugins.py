import logging
import os
from json import loads

from slackbot.bot import respond_to

from attendance_slack.akashi.dakoku_type import DakokuType
from attendance_slack.akashi.exception import (
    BadShukkinStateException,
    BadTaikinStateException,
    UserNotFoundException,
)
from attendance_slack.akashi.use_case import AkashiUseCase
from attendance_slack.aws.ssm_client import AwsSsmClient
from attendance_slack.token_store_type import TokenStoreType


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
    user_name = message._client.get_user(message.body["user"])["name"]
    logging.info(
        "start: dakoku type: user_name[{}] dakoku_type[{}]".format(
            user_name, dakoku_type.name
        )
    )
    message.react("akashi")
    try:
        # tokenが置かれている場所をconfigで切り替え可能にする
        token_store = os.getenv("TOKEN_STORE", TokenStoreType.LOCAL.value)
        # localの場合、環境変数からの取得になる.
        if token_store == TokenStoreType.LOCAL.value:
            AkashiUseCase.dakoku(
                user_name, dakoku_type, loads(os.getenv("AKASHI_USER_INFO"))
            )
        # aws_ssmの場合, awsのssmから取得する。追加でparameter nameやkey_idが必要となる。
        elif token_store == TokenStoreType.AWS_SSM.value:
            ssm_client = AwsSsmClient(os.getenv("AWS_PROFILE"))
            param = ssm_client.get_parameter(os.getenv("PSTORE_NAME"))
            AkashiUseCase.dakoku(user_name, dakoku_type, loads(param))
    except UserNotFoundException:
        logging.warning("user not found. user_name[{}]".format(user_name))
        message.reply("ぜひ管理者にユーザ登録してもらってね :hugging_face:")
    except BadShukkinStateException:
        logging.warning(
            "Bad shukkin state exception. user_name[{}]".format(user_name),
            exc_info=True,
        )
        message.reply("前営業日の退勤の打刻をしていないかも :thinking_face:")
    except BadTaikinStateException:
        logging.warning(
            "Bad taikin state exception. user_name[{}]".format(user_name), exc_info=True
        )
        message.reply("出勤の打刻をしていないかも :thinking_face:")
    except Exception:
        logging.error("unexcept exception...!!", exc_info=True)
        message.reply("技術的な問題で打刻できませんでした :cry: 管理者が解析します :pray:")
        message.react("damedatta")
    else:
        logging.info(
            "finish: dakoku type: user_name[{}] dakoku_type[{}]".format(
                user_name, dakoku_type.name
            )
        )
        message.react("done")
