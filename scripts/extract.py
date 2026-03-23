from ucimlrepo import fetch_ucirepo
import pandas as pd

# Fetch the Dataset
data = fetch_ucirepo(id = 352)

df = data.data.original

# Save the dataset to a CSV file
df.to_csv(r"C:\Users\biswa\Downloads\Projects & Notes Files\Python Projects & Notes File\online_retail_eda_analysis_project\data\raw\retail_dataset.csv", index=False)

print("Data Extracted and Saved to CSV file successfully!")