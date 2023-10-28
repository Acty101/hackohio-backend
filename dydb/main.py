import boto3
import os
import typing

class DYDB:
    def __init__(
        self,
        table: str = None,
        aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID", None),
        aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY", None),
        region_name=os.environ.get("AWS_DEFAULT_REGION", None),
    ) -> None:
        self.table = table
        self.dydb = boto3.client(
            "dynamodb",
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            region_name=region_name,
        )

    def create(self, data: typing.Dict) -> None:
        self.dydb.put_item(TableName=self.table, Item=self.mapper(data)["M"])

    def mapper(self, data: typing.Any) -> typing.Dict:
        """Map dictionary data to DynamoDB-support data scheme recursively"""
        datatype = type(data)
        if datatype == str:
            return {"S": data}
        elif datatype == bool:
            return {"BOOL": data}
        elif datatype == float or datatype == int:
            return {"N": str(data)}
        elif datatype == list:
            return {"L": [self.mapper(x) for x in data]}
        elif datatype == dict:
            _map = {}
            for k, v in data.items():
                _map[k] = self.mapper(v)
            return {"M": _map}