import logging
from json import dumps, loads
from urllib import error, request, parse
import os
from attendance_slack.akashi.dakoku_type import DakokuType


class AkashiClient():

    def __init__(self, user_name):
        # TODO: 環境変数系の値はconfig.pyとかにまとめる
        self.company_id = os.getenv("AKASHI_COMPANY_ID")
        # user情報はmapで{"slack_user_name": "token"}の形式でもらう
        user_map = loads(os.getenv("AKASHI_USER_INFO"))
        self.token = user_map[user_name]
        self.url = "https://atnd.ak4.jp"
        self.base_path = "api/cooperation/{}".format(self.company_id)

    def dakoku(self, dakoku_type):
        """打刻APIを発行する.
            dakoku_type: dakoku_type.DakokuType
        """
        if dakoku_type not in DakokuType:
            raise EnvironmentError("type is invalid. {}".format(dakoku_type))

        # request msgの設定
        request_body = {"type": dakoku_type.value}
        # TODO ここもっとキレイに書きたい
        url = parse.urljoin(self.url, self.base_path + "/stamps" + "?token={}".format(self.token))
        req = request.Request(url, dumps(request_body).encode(), method="POST")
        logging.debug(req)

        # requestの発行
        try:
            with request.urlopen(req) as res:
                logging.info("request is ok. {}".format(res.read()))
        except error.HTTPError as e:
            logging.error("not return OK response from akashi. code:{} ,reason: {}".format(e.code, e.read().decode('utf-8')))
            raise e
