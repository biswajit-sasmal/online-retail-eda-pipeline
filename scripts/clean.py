import pandas as pd

# Load Data To Pandas Dataframe
df = pd.read_csv(r"C:\Users\biswa\Downloads\Projects & Notes Files\Python Projects & Notes File\online_retail_eda_analysis_project\data\raw\retail_dataset.csv",
dtype={'InvoiceNo': str, 'StockCode': str, 'CustomerID': str , 'Description': str})

# Convert InvoiceDate to Proper Date Format
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce').dt.floor('D') 

# Remove Invalid Quantity and Price
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] >= 1)]

# Remove All the Cancelled Invoices
df = df[~df['InvoiceNo'].str.lower().str.startswith('c', na=False)] 

# Remove all Extra spaces & Special Characters (Non - ASCII Characters) from Description  
df['Description'] = df['Description'].str.replace(r'[^\x20-\x7E]', '', regex=True).str.replace(r'\s+' , ' ' , regex = True).str.strip().str.upper()

# Remove Extra spaces from InvoiceNo Column
df['InvoiceNo'] = df['InvoiceNo'].str.strip()

# Fix Description for each StockCode by Replacing Most Frequent Description for each StockCode
mapping = df.groupby(by = 'StockCode')['Description'].agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'UNKNOWN').reset_index().rename(columns = {'Description' : 'Description_MostFrequent'})

df = pd.merge(df , mapping , on = 'StockCode' , how = 'left')

df['Description'] = df['Description_MostFrequent']

df.drop(columns = ['Description_MostFrequent'] , inplace = True)

# Remove All the Duplicate Records
df = df.drop_duplicates(keep='first')

# feature Engineering
# Create TotalPrice Column  
df['TotalPrice'] = df['Quantity'] * df['UnitPrice'] 
# Create Year and Month Column
df['Year'] = pd.to_datetime(df['InvoiceDate']).dt.year 
# Add Month Number Column
df['MonthNumber'] = df['InvoiceDate'].dt.month
# Add Month Name Column     
df['Month'] = pd.to_datetime(df['InvoiceDate']).dt.month_name()

# Save Cleaned Data to CSV
df.to_csv(r"C:\Users\biswa\Downloads\Projects & Notes Files\Python Projects & Notes File\online_retail_eda_analysis_project\data\processed\cleaned_retail_dataset.csv", index=False)

# Print Summary of Cleaned Data
print("Data Cleaning Completed!")
print(f"Total Records After Cleaning: {len(df)}")
print(f"Total Unique Customers: {df['CustomerID'].nunique()}")  
print(f"Total Unique Invoices: {df['InvoiceNo'].nunique()} ")
print(f"Total Unique Products: {df['StockCode'].nunique()} ")
print(f"Total Unique Descriptions: {df['Description'].nunique()}")
