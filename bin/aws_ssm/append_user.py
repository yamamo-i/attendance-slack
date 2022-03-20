import argparse
from json import loads, dumps
from attendance_slack.aws.ssm_client import AwsSsmClient

p = argparse.ArgumentParser()
p.add_argument('-u', '--user-name', required=True, help='追加するuser名')
p.add_argument("-t", "--token", required=True, help="userのtoken")

p.add_argument('-p', '--profile', required=True, help='利用するaws profile')
p.add_argument('-n', '--name', required=True, help='userのtokenが配置されてるAWS SSMのname')
p.add_argument('-k', '--key-id', required=True, help='AWS SSMで暗号化しているKMS key id')
p.add_argument('-r', '--raw', action='store_true', help='user情報をjsonのまま出力する')
args = p.parse_args()

ssm_client = AwsSsmClient(args.profile)
user_info = loads(ssm_client.get_parameter(args.name))
user_info[args.user_name] = args.token
user_info_str = dumps(user_info)
if args.raw:
    print(user_info_str)
else:
    ssm_client.put_parameter(args.name, user_info_str, args.key_id)
