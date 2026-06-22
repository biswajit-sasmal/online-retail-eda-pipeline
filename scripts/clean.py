def clean_data():
    """
    Reads the raw CSV from data/raw/retail_dataset.csv,
    cleans it (removes bad rows, fixes columns, adds features),
    saves the result to data/processed/cleaned_retail_dataset.csv,
    and RETURNS the cleaned DataFrame so notebooks can use it directly.

    Returns:
        pd.DataFrame : the fully cleaned and feature-enriched DataFrame
    """

    # ── Import Libraries ────────────────────────────────────────────────────
    import pandas as pd       # for working with tables (DataFrames)
    from pathlib import Path  # for building file paths safely

    # ── Step 1: Build File Paths Dynamically ───────────────────────────────
    #
    # Same trick as extract.py:
    # Path(__file__)  → this file's location (.../scripts/clean.py)
    # .resolve()      → full absolute path
    # .parent         → goes up to .../scripts/
    # .parent         → goes up to .../online_retail_eda_analysis_project/
    #
    # This means your code works on ANY computer without changing hardcoded paths ✅

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Path to the raw file that extract.py already created
    INPUT_FILE  = BASE_DIR / "data" / "raw" / "retail_dataset.csv"

    # Path to the folder where we'll save the cleaned file
    OUTPUT_DIR  = BASE_DIR / "data" / "processed"
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)   # create folder if missing

    # Full path for the cleaned output CSV
    OUTPUT_FILE = OUTPUT_DIR / "cleaned_retail_dataset.csv"

    # ── Step 2: Load the Raw CSV ────────────────────────────────────────────
    #
    # We tell pandas what DATA TYPE each column should be as we load it.
    # By default pandas tries to guess — but sometimes it guesses wrong.
    #
    # dtype={...} lets us FORCE the correct type:
    #   'InvoiceNo'  : str → keep as text (some have letters like 'C12345')
    #   'StockCode'  : str → keep as text (not a number to do math on)
    #   'CustomerID' : str → keep as text (IDs are labels, not numbers)
    #   'Description': str → obviously text

    df = pd.read_csv(INPUT_FILE, dtype={
        'InvoiceNo'  : str,
        'StockCode'  : str,
        'CustomerID' : str,
        'Description': str
    })
    print(f"Raw data loaded. Shape: {df.shape}")

    # ── Step 3: Fix the Date Column ─────────────────────────────────────────
    #
    # In the CSV, InvoiceDate is just a string like "2010-12-01 08:26:00"
    # We need to convert it to a proper date object so we can sort/filter by date.
    #
    # pd.to_datetime()  → converts string → datetime
    # errors='coerce'   → if a value can't be converted, make it NaT (Not a Time)
    #                      instead of crashing the whole program
    # .dt.floor('D')    → removes the time part (keeps only the date: 2010-12-01)
    #                      'D' means "Day" — so we floor to day precision

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce').dt.floor('D')

    # ── Step 4: Remove Bad Quantity and Price Rows ──────────────────────────
    #
    # Some rows have Quantity = 0 or negative (returns/errors)
    # Some rows have UnitPrice = 0 (free items or data errors)
    #
    # We KEEP only rows where:
    #   Quantity  > 0    → at least 1 item was sold
    #   UnitPrice >= 1   → item costs at least £1
    #
    # The & means BOTH conditions must be true at the same time

    df = df[(df['Quantity'] > 0) & (df['UnitPrice'] >= 1)]

    # ── Step 5: Remove Cancelled Invoices ───────────────────────────────────
    #
    # Cancelled orders have InvoiceNo starting with 'C' (e.g., 'C536379')
    # We want to REMOVE these — they're not real sales.
    #
    # df['InvoiceNo'].str.lower()           → make lowercase so 'C' and 'c' both match
    # .str.startswith('c', na=False)        → True if it starts with 'c'
    #                                          na=False → treat missing values as False
    # ~ (tilde)                             → means NOT — so we KEEP rows that do NOT start with 'c'

    df = df[~df['InvoiceNo'].str.lower().str.startswith('c', na=False)]

    # ── Step 6: Clean the Description Column ───────────────────────────────
    #
    # Descriptions can have messy characters, extra spaces, and mixed case.
    # We clean it in 4 steps (chained together):
    #
    # 1. .str.replace(r'[^\x20-\x7E]', '', regex=True)
    #    → Remove any character that is NOT a standard printable ASCII character
    #      \x20 = space, \x7E = ~ (tilde)
    #      So we keep only normal English letters, numbers, punctuation
    #
    # 2. .str.replace(r'\s+', ' ', regex=True)
    #    → Replace multiple spaces/tabs with a single space
    #      "RED  WOOLLY   HOTTIE" → "RED WOOLLY HOTTIE"
    #
    # 3. .str.strip()
    #    → Remove leading and trailing spaces
    #      "  CANDLE  " → "CANDLE"
    #
    # 4. .str.upper()
    #    → Make everything UPPERCASE for consistency
    #      "red candle" → "RED CANDLE"

    df['Description'] = (
        df['Description']
        .str.replace(r'[^\x20-\x7E]', '', regex=True)
        .str.replace(r'\s+', ' ', regex=True)
        .str.strip()
        .str.upper()
    )

    # ── Step 7: Clean InvoiceNo Column ─────────────────────────────────────
    #
    # Sometimes InvoiceNo values have accidental spaces like " 536365"
    # .str.strip() removes leading and trailing whitespace

    df['InvoiceNo'] = df['InvoiceNo'].str.strip()

    # ── Step 8: Fix Inconsistent Descriptions per StockCode ────────────────
    #
    # The SAME product (same StockCode) sometimes has DIFFERENT descriptions
    # e.g., StockCode "85123A" might appear as:
    #   - "WHITE HANGING HEART T-LIGHT HOLDER"
    #   - "white hanging heart t-light"
    #   - "WHITE HEART LIGHT HOLDER"
    #
    # We fix this by finding the MOST COMMON description for each StockCode
    # and using ONLY that one everywhere.
    #
    # Step A: Group rows by StockCode, then find the most frequent Description
    # .agg(lambda x: x.mode().iloc[0] ...)
    #   → x.mode() gives the most frequent value(s) as a list
    #   → .iloc[0] takes the first one (in case of a tie)
    #   → if no mode exists (empty), use 'UNKNOWN'
    # .reset_index() → converts the result back into a regular DataFrame
    # .rename(...)   → rename the column so we can tell it apart from the original

    mapping = (
        df.groupby('StockCode')['Description']
        .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'UNKNOWN')
        .reset_index()
        .rename(columns={'Description': 'Description_MostFrequent'})
    )

    # Step B: Merge this mapping back into the main DataFrame
    # pd.merge(..., on='StockCode', how='left')
    #   → Match each row's StockCode with the mapping table
    #   → 'left' means: keep ALL rows from df, even if there's no match
    # Now df has an extra column: 'Description_MostFrequent'

    df = pd.merge(df, mapping, on='StockCode', how='left')

    # Step C: Replace the old Description with the standardized one
    df['Description'] = df['Description_MostFrequent']

    # Step D: Remove the helper column — we don't need it anymore
    df.drop(columns=['Description_MostFrequent'], inplace=True)

    # ── Step 9: Remove Duplicate Rows ──────────────────────────────────────
    #
    # If the exact same row appears more than once, keep only the FIRST occurrence
    # keep='first' → keep the first copy, drop the rest

    df = df.drop_duplicates(keep='first')

    # ── Step 10: Feature Engineering (Add New Useful Columns) ───────────────
    #
    # We CREATE new columns that will help us analyse the data later.
    #
    # TotalPrice  → how much money was made for each line item
    #               (how many items × price per item)
    #
    # Year        → extract just the year from InvoiceDate (e.g., 2010, 2011)
    #
    # MonthNumber → extract month as a number (1=Jan, 2=Feb, ..., 12=Dec)
    #               useful for sorting
    #
    # Month       → extract month as a name (e.g., "January", "February")
    #               useful for labels on charts

    df['TotalPrice']  = df['Quantity'] * df['UnitPrice']
    df['Year']        = pd.to_datetime(df['InvoiceDate']).dt.year
    df['MonthNumber'] = df['InvoiceDate'].dt.month
    df['Month']       = pd.to_datetime(df['InvoiceDate']).dt.month_name()

    # ── Step 11: Save Cleaned Data to CSV ──────────────────────────────────
    #
    # index=False → don't write the row numbers as a column in the CSV

    df.to_csv(OUTPUT_FILE, index=False)

    # ── Step 12: Print a Summary of What We Did ────────────────────────────
    print("\n✅ Data Cleaning Completed!")
    print(f"   Cleaned file saved to  : {OUTPUT_FILE}")
    print(f"   Total Records          : {len(df):,}")
    print(f"   Total Unique Customers : {df['CustomerID'].nunique():,}")
    print(f"   Total Unique Invoices  : {df['InvoiceNo'].nunique():,}")
    print(f"   Total Unique Products  : {df['StockCode'].nunique():,}")
    print(f"   Total Unique Descriptions: {df['Description'].nunique():,}")

    # ── Step 13: Return the cleaned DataFrame ──────────────────────────────
    #
    # This is the KEY change from the original!
    # By returning df, the notebook can do:
    #   df = clean_data()
    # ...and immediately start using the cleaned data WITHOUT reading the CSV again.

    return df
