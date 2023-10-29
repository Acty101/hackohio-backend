from shared_utils import get_prompt
from langChain import LangChainURL

path = "./config/prompt.txt"
cat_path = "./config/supercategory.yaml"

prompt = get_prompt(path, cat_path)

model = LangChainURL(prompt)
print(model.infer("plastic bottle, paper, cardboard"))
