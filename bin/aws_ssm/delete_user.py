import argparse
from json import dumps, loads

from attendance_slack.aws.ssm_client import AwsSsmClient

p = argparse.ArgumentParser()
p.add_argument("-u", "--user-name", required=True, help="追加するuser名")

p.add_argument("-p", "--profile", required=True, help="利用するaws profile")
p.add_argument("-n", "--name", required=True, help="userのtokenが配置されてるAWS SSMのname")
p.add_argument("-k", "--key-id", required=True, help="AWS SSMで暗号化しているKMS key id")
args = p.parse_args()

ssm_client = AwsSsmClient(args.profile)
user_info = loads(ssm_client.get_parameter(args.name))
if user_info.pop(args.user_name, None) is None:
    print(f"{args.user_name} is not exist.")
    exit(1)
user_info_str = dumps(user_info)
ssm_client.put_parameter(args.name, user_info_str, args.key_id)
