import argparse
from attendance_slack.akashi.client import AkashiClient
from base64 import b64decode, b64encode
from json import loads as json_loads, dumps
from yaml import FullLoader, load as yaml_load


p = argparse.ArgumentParser()
p.add_argument("-c", "--config", required=True, help="k8sのsecret yamlのファイルパス")
p.add_argument("-d", "--dry-run", action="store_true", help="tokenの再発行をせずにユーザ情報のjsonを出力する")
args = p.parse_args()

with open(args.config) as file:
    secret = yaml_load(file, Loader=FullLoader)
    user_info = json_loads(b64decode(secret["data"]["akashi_user_info"]))
    company_id = b64decode(secret["data"]["akashi_company_id"]).decode("utf-8")
    if args.dry_run:
        print(dumps(user_info))
    else:
        new_user_info = {}
        for user_name, _ in user_info.items():
            new_token = AkashiClient(user_name, company_id, user_info).update_token()
            user_info[user_name] = new_token
        print(b64encode(dumps(user_info).encode("utf-8")).decode("utf-8"))
