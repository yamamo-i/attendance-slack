import argparse
from base64 import b64decode, b64encode
from json import loads as json_loads, dumps
from yaml import FullLoader, load as yaml_load


p = argparse.ArgumentParser()
p.add_argument("-c", "--config", required=True, help="k8sのsecret yamlのファイルパス")
p.add_argument("-n", "--name", required=True, help="追加するuser名")
p.add_argument("-t", "--token", required=True, help="userのtoken")
p.add_argument("-r", "--raw", action="store_true", help="user情報をjsonのまま出力する")
args = p.parse_args()

with open(args.config) as file:
    secret = yaml_load(file, Loader=FullLoader)
    user_info = json_loads(b64decode(secret["data"]["akashi_user_info"]))
    user_info[args.name] = args.token
    user_info_str = dumps(user_info)
    if (args.raw):
        print(user_info_str)
    else:
        print(b64encode(user_info_str.encode('utf-8')))
