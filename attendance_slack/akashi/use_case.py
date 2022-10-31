import os
from datetime import datetime, timedelta, timezone

from attendance_slack.akashi.client import AkashiClient
from attendance_slack.akashi.dakoku_type import DakokuType
from attendance_slack.akashi.exception import (
    BadShukkinStateException,
    BadTaikinStateException,
)


class AkashiUseCase:
    @classmethod
    def dakoku(cls, user_name: str, dakoku_type: str, user_info: dict) -> None:
        """Akashiに打刻(出勤/退勤)を発行する
        user_name: str dakokuするuserの名前
        dakoku_type: akashi.dakoku_type.DakokuType
        """
        client = AkashiClient(user_name, os.getenv("AKASHI_COMPANY_ID"), user_info)
        # 直前の打刻状態をチェックする
        JST = timezone(timedelta(hours=+9), "JST")
        end_date = datetime.now(JST)
        if dakoku_type == DakokuType.SHUKKIN:
            # 出勤: 直近1ヶ月の出退勤の直前の打刻タイプが退勤であること
            # MEMO: 1ヶ月であることは目安であり、長期休暇の場合は考慮しない
            start_date = end_date - timedelta(days=31)
            stamps = cls.__get_target_stamps(client, start_date, end_date)
            if len(stamps) == 0 or stamps[-1]["type"] != DakokuType.TAIKIN:
                raise BadShukkinStateException(
                    "Bad Stamp State. {}".format(stamps[-1:])
                )
        elif dakoku_type == DakokuType.TAIKIN:
            # 退勤: 直前1日の範囲(日付跨ぎ対応)で直前の打刻タイプが出勤であること
            # MEMO: 2日であることは目安であり、48時間以上稼働する場合は考慮しない
            start_date = end_date - timedelta(days=2)
            stamps = cls.__get_target_stamps(client, start_date, end_date)
            if len(stamps) == 0 or stamps[-1]["type"] != DakokuType.SHUKKIN:
                raise BadTaikinStateException("Bad Stamp State. {}".format(stamps[-1:]))
        else:
            raise Exception("DakokuType is not found. {}".format(dakoku_type))

        client.dakoku(dakoku_type)

    @classmethod
    def __get_target_stamps(cls, client, start_date, end_date):
        """stampsを出勤/退勤の打刻情報だけを取得する.

        client: AkashiClientオブジェクト
        start_type: datetime
        end_type: datetime
        return: list(stamps)
        """
        res = client.get_stamps(start_date, end_date)
        stamps = res["response"]["stamps"]
        # TODO: DakokuTypeが他の状態も使うとエラーになる...
        return [stamp for stamp in stamps if stamp["type"] in list(DakokuType)]
