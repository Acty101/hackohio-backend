from shared_utils import get_prompt
from langChain import LangChainURL
from dotenv import load_dotenv

load_dotenv()

path = "./config/prompt.txt"
cat_path = "./config/supercategory.yaml"

prompt = get_prompt(path, cat_path)

model = LangChainURL(prompt)
print(model.infer(["drink can", "drink can", "clear plastic bottle", "clear plastic bottle", "drink can", "clear plastic bottle"]))
print(model.sc_count)
