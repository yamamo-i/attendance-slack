import argparse
from json import dumps, loads

from attendance_slack.akashi.client import AkashiClient
from attendance_slack.aws.ssm_client import AwsSsmClient

p = argparse.ArgumentParser()
p.add_argument("-n", "--name", required=True, help="userのtokenが配置されてるAWS SSMのname")
p.add_argument("-k", "--key-id", required=True, help="AWS SSMで暗号化しているKMS key id")
p.add_argument("-c", "--company-id", required=True, help="akashiに設定されたcompany_id")
p.add_argument(
    "-d", "--dry-run", action="store_true", help="tokenの再発行をせずにユーザ情報のjsonを出力する"
)
args = p.parse_args()

ssm_client = AwsSsmClient()
user_info = loads(ssm_client.get_parameter(args.name))
if args.dry_run:
    print(dumps(user_info))
else:
    new_user_info = {}
    for user_name, _ in user_info.items():
        try:
            new_token = AkashiClient(
                user_name, args.company_id, user_info
            ).update_token()
            new_user_info[user_name] = new_token
            print(f"updated token {user_name}.")
        except Exception:
            # 退職者は更新できないので管理tokenから抹消
            # TODO AWS SSMはバージョニングされるので、今は`退職者`の厳密なハンドリングはしていない
            print(f"cannot update token. {user_name}")
    ssm_client.put_parameter(args.name, dumps(new_user_info), args.key_id)
