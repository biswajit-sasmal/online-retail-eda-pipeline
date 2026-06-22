def extract_data():
    """
    Downloads the Online Retail dataset from UCI ML Repository
    and saves it as a CSV file inside  data/raw/retail_dataset.csv
    
    Returns:
        str : a message telling you where the file was saved
    """

    # ── Import Libraries ────────────────────────────────────────────────────
    from ucimlrepo import fetch_ucirepo   # special library to download UCI datasets
    import pandas as pd                   # pandas helps us work with tables (DataFrames)
    from pathlib import Path              # pathlib helps us build file paths safely

    # ── Step 1: Find WHERE this script lives and build paths from there ─────
    #
    # Imagine your script lives at:
    #   C:/Projects/online_retail_eda_analysis_project/scripts/extract.py
    #
    # Path(__file__)  → gives:  .../scripts/extract.py
    # .resolve()      → converts to a FULL absolute path (removes any ".." shortcuts)
    # .parent         → goes UP one folder → .../scripts/
    # .parent         → goes UP again      → .../online_retail_eda_analysis_project/
    #
    # So BASE_DIR always points to the ROOT of your project, no matter
    # which computer or folder you move this project to. ✅

    BASE_DIR = Path(__file__).resolve().parent.parent

    # Now build the path to the "data/raw" folder from the project root
    # The "/" operator in pathlib means "join this folder name onto the path"
    # So this becomes: .../online_retail_eda_analysis_project/data/raw
    OUTPUT_DIR = BASE_DIR / "data" / "raw"

    # Create the folder if it doesn't exist yet
    # parents=True  → also create "data/" if it's missing (not just "raw/")
    # exist_ok=True → don't throw an error if the folder already exists
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Build the full path to the CSV file we're about to create
    # Result: .../online_retail_eda_analysis_project/data/raw/retail_dataset.csv
    OUTPUT_FILE = OUTPUT_DIR / "retail_dataset.csv"

    # ── Step 2: Download the dataset from UCI ML Repository ─────────────────
    #
    # The UCI ML Repository has hundreds of datasets.
    # Each one has a unique ID number.
    # The "Online Retail" dataset has ID = 352.
    # fetch_ucirepo(id=352) goes online and downloads it for us.

    print("Fetching dataset from UCI ML Repository...")
    data = fetch_ucirepo(id=352)

    # data.data.original gives us the raw, original table as a pandas DataFrame
    # A DataFrame is like an Excel table — rows and columns
    df = data.data.original

    # df.shape gives us (number_of_rows, number_of_columns)
    # We print this so we can confirm the download worked
    print(f"Dataset fetched successfully! Shape: {df.shape}")

    # ── Step 3: Save the DataFrame to a CSV file ────────────────────────────
    #
    # df.to_csv() saves the table as a .csv file
    # index=False means: do NOT write the row numbers (0, 1, 2, ...) as a column
    #                    we don't need them — the data already has its own columns

    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Raw data saved to: {OUTPUT_FILE}")

    # ── Step 4: Return a success message ────────────────────────────────────
    # This message will be printed in the notebook when we call this function
    return f"Data saved to: {OUTPUT_FILE}"