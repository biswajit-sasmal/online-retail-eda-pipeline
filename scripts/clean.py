import pandas as pd
from pathlib import Path

# ── Build Paths Dynamically ─────────────────────────────────────────────────
# Find the folder where THIS script lives
BASE_DIR = Path(__file__).resolve().parent

# Input file  → data/raw/retail_dataset.csv  (created by extract.py)
INPUT_FILE = BASE_DIR / "data" / "raw" / "retail_dataset.csv"

# Output file → data/processed/cleaned_retail_dataset.csv
OUTPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)  # Create folder if it doesn't exist
OUTPUT_FILE = OUTPUT_DIR / "cleaned_retail_dataset.csv"

# ── Load Data ───────────────────────────────────────────────────────────────
df = pd.read_csv(INPUT_FILE, dtype={
    'InvoiceNo'  : str,
    'StockCode'  : str,
    'CustomerID' : str,
    'Description': str
})

# ── Convert InvoiceDate to Proper Date Format ───────────────────────────────
df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce').dt.floor('D')

# ── Remove Invalid Quantity and Price ───────────────────────────────────────
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] >= 1)]

# ── Remove All Cancelled Invoices ───────────────────────────────────────────
df = df[~df['InvoiceNo'].str.lower().str.startswith('c', na=False)]

# ── Clean Description Column ────────────────────────────────────────────────
# Remove special/non-ASCII characters, fix extra spaces, uppercase everything
df['Description'] = (
    df['Description']
    .str.replace(r'[^\x20-\x7E]', '', regex=True)
    .str.replace(r'\s+', ' ', regex=True)
    .str.strip()
    .str.upper()
)

# ── Clean InvoiceNo Column ──────────────────────────────────────────────────
df['InvoiceNo'] = df['InvoiceNo'].str.strip()

# ── Fix Description: Use Most Frequent Description per StockCode ────────────
mapping = (
    df.groupby('StockCode')['Description']
    .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'UNKNOWN')
    .reset_index()
    .rename(columns={'Description': 'Description_MostFrequent'})
)

df = pd.merge(df, mapping, on='StockCode', how='left')
df['Description'] = df['Description_MostFrequent']
df.drop(columns=['Description_MostFrequent'], inplace=True)

# ── Remove Duplicate Records ────────────────────────────────────────────────
df = df.drop_duplicates(keep='first')

# ── Feature Engineering ─────────────────────────────────────────────────────
df['TotalPrice']  = df['Quantity'] * df['UnitPrice']
df['Year']        = pd.to_datetime(df['InvoiceDate']).dt.year
df['MonthNumber'] = df['InvoiceDate'].dt.month
df['Month']       = pd.to_datetime(df['InvoiceDate']).dt.month_name()

# ── Save Cleaned Data ───────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)

# ── Summary ─────────────────────────────────────────────────────────────────
print("Data Cleaning Completed!")
print(f"Cleaned file saved to : {OUTPUT_FILE}")
print(f"Total Records          : {len(df)}")
print(f"Total Unique Customers : {df['CustomerID'].nunique()}")
print(f"Total Unique Invoices  : {df['InvoiceNo'].nunique()}")
print(f"Total Unique Products  : {df['StockCode'].nunique()}")
print(f"Total Unique Descriptions: {df['Description'].nunique()}")
