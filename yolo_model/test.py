import pandas as pd

# Sample DataFrame
data = {'A': [1, 2, 3],
        'B': ['apple', 'banana', 'cherry'],
        'C': [4.0, 5.0, 6.0]}

df = pd.DataFrame(data)

# Create a list of dictionaries
result_list = []

for index, row in df.iterrows():
    result_dict = {'name': row['A'], 'bbox': row['B']}
    result_list.append(result_dict)

print(result_list)





