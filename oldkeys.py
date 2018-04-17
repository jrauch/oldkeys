import boto3
from datetime import datetime, timezone
import argparse

parser = argparse.ArgumentParser(description="Check for old AWS keys")
parser.add_argument("-d", type=int, help="keys greater than or equal to D days old (default: 90)", default=90)
args = parser.parse_args()
client = boto3.client("iam")

accesskeys = client.list_access_keys()
today = datetime.now(timezone.utc)

for accesskey in accesskeys["AccessKeyMetadata"]:
    lastused = client.get_access_key_last_used(AccessKeyId=accesskey["AccessKeyId"])
    lastdate = lastused["AccessKeyLastUsed"]["LastUsedDate"]
    age = (today - lastdate).days
    if age >= args.d:
        print("{},{},{}".format(lastused["UserName"], accesskey["AccessKeyId"], age))
