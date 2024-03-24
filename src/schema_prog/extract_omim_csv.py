import pandas as pd
import json 

csv_file = 'data/OMIM/omim_onto.csv'
df = pd.read_csv(csv_file)
schema = {col: str(dtype) for col, dtype in df.dtypes.items()}
with open('data/OMIM/omim_schema.json', 'w') as f:
	json.dump(schema, f, indent=4)