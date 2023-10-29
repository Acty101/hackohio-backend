from dydb import DYDB
from dotenv import load_dotenv
import os
import uuid

load_dotenv()


table_name = os.environ.get("DYDB_TABLE")
dydbc = DYDB(table_name)
data = {"id": str(uuid.uuid4()), "supercategory": "paper", "instances": 4, "location":"39.7589, -84.1916"}

dydbc.create(data)