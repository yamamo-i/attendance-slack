import argparse
from base64 import b64decode, b64encode
from json import dumps
from json import loads as json_loads

from yaml import FullLoader
from yaml import load as yaml_load

p = argparse.ArgumentParser()
p.add_argument("-c", "--config", required=True, help="k8sのsecret yamlのファイルパス")
p.add_argument("-n", "--name", required=True, help="削除対象のuser名")
args = p.parse_args()

with open(args.config) as file:
    secret = yaml_load(file, Loader=FullLoader)
    user_info = json_loads(b64decode(secret["data"]["akashi_user_info"]))
    if user_info.pop(args.name) is None:
        print(f"{args.name} is not exist.")
        exit(1)
    print(b64encode(dumps(user_info).encode("utf-8")).decode("utf-8"))
