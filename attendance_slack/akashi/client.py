from datetime import datetime
import logging
from json import dumps, loads
from urllib import error, request, parse
from attendance_slack.akashi.dakoku_type import DakokuType
from attendance_slack.akashi.exception import UserNotFoundException


class AkashiClient():

    def __init__(self, user_name, company_id, user_info):
        # TODO: 環境変数系の値はconfig.pyとかにまとめる
        self.company_id = company_id
        # user情報はmapで{"slack_user_name": "token"}の形式でもらう
        try:
            self.token = user_info[user_name]
        except KeyError as e:
            raise UserNotFoundException(
                "Not a registered user: {}".format(user_name), e)
        self.url = "https://atnd.ak4.jp"
        self.base_path = "api/cooperation"

    def dakoku(self, dakoku_type):
        """打刻APIを発行する.
            dakoku_type: dakoku_type.DakokuType
        """
        if dakoku_type not in DakokuType:
            raise EnvironmentError("type is invalid. {}".format(dakoku_type))

        # request msgの設定
        request_body = {"type": dakoku_type.value}
        # TODO ここもっとキレイに書きたい
        url = parse.urljoin(self.url, self.base_path +
                            "/{}/stamps?token={}".format(self.company_id, self.token))
        req = request.Request(url, dumps(request_body).encode(), method="POST")
        self._request_api(req)

    def get_stamps(self, start_date, end_date):
        """打刻情報を取得するAPIを発行する.

            https://akashi.zendesk.com/hc/ja/articles/115000475854-AKASHI-%E5%85%AC%E9%96%8BAPI-%E4%BB%95%E6%A7%98#get_stamp
            start_type: datetime
            end_type: datetime
            return: dict response body
        """
        _date_format = "%Y%m%d%H%M%S"
        url = parse.urljoin(self.url, self.base_path + "/{}/stamps?token={}&start_date={}&end_date={}".format(
            self.company_id, self.token, datetime.strftime(start_date, _date_format), datetime.strftime(end_date, _date_format)))
        req = request.Request(url, method="GET")
        return loads(self._request_api(req))

    def update_token(self):
        """Akashiのtokenを更新する.

            https://akashi.zendesk.com/hc/ja/articles/115000475854-AKASHI-%E5%85%AC%E9%96%8BAPI-%E4%BB%95%E6%A7%98#get_token
            return: str 新規発行したtoken
        """
        url = parse.urljoin(self.url, self.base_path +
                            "/token/reissue/{}?token={}".format(self.company_id, self.token))
        req = request.Request(url, None, method="POST")
        res_body = loads(self._request_api(req))
        return res_body["response"]["token"]

    def _request_api(self, req):
        """AkashiへのAPIを発行.
            req: urllib.request.Request
            return: str responseのbody
        """
        logging.debug(req)
        try:
            body = None
            with request.urlopen(req) as res:
                body = res.read()
                logging.debug("request is ok. response body: {}".format(body))
            return body
        except error.HTTPError as e:
            logging.error("return NG response from akashi. code:{} ,reason: {}".format(
                e.code, e.read().decode('utf-8')))
            raise e
