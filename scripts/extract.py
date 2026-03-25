from ucimlrepo import fetch_ucirepo
import pandas as pd
from pathlib import Path

# ── Step 1: Build the output path dynamically ──────────────────────────────
# Path(__file__) → the current script's full file path
# .resolve()     → convert to an absolute path (no "../" tricks)
# .parent        → go up one folder (the folder where this script lives)

BASE_DIR = Path(__file__).resolve().parent.parent

# Now build the path to the "data/raw" folder relative to this script
OUTPUT_DIR = BASE_DIR / "data" / "raw"

# Create all missing folders automatically (no error if they already exist)
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Full path to the final CSV file
OUTPUT_FILE = OUTPUT_DIR / "retail_dataset.csv"

# ── Step 2: Fetch the dataset ───────────────────────────────────────────────
print("Fetching dataset from UCI ML Repository...")

data = fetch_ucirepo(id=352)
df = data.data.original

print(f"Dataset fetched successfully! Shape: {df.shape}")  # (rows, columns)

# ── Step 3: Save to CSV ─────────────────────────────────────────────────────
df.to_csv(OUTPUT_FILE, index=False)

print(f"Data saved to: {OUTPUT_FILE}")