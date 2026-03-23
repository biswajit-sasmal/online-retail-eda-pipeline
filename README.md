# 🛍️ Retail Sales Analysis Project

A concise data analysis project that explores retail sales transactions to surface business patterns and actionable insights.

---

## 📚 Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tools & Technology](#2-tools--technology)
3. [How to Run This Project](#3-how-to-run-this-project)
4. [Key Insights](#4-key-insights)
5. [Recommendations](#5-recommendations)
6. [Dataset Acknowledgement](#6-dataset-acknowledgement)
7. [Thank You](#7-thank-you)

---

## 1. Project Overview

This project analyzes a **retail store's sales data** to answer practical business questions, such as:

- 📦 Which products sell the most?
- 🌍 Which countries bring in the most money?
- 🔁 Who are the most loyal customers?
- 📅 How did sales change month by month in 2011?

The workflow includes cleaning raw data, exploratory data analysis (EDA), visualization, and customer segmentation using **RFM Analysis** *(details below)*.

> 💡 **What is RFM?** RFM stands for **Recency** (how recently a customer made a purchase), **Frequency** (how often they buy), and **Monetary** (how much they spend). It is a common technique to identify high-value customers.

### 📁 Project folder structure

```
├── data/
│   ├── raw/                  ← Original, untouched data
│   └── processed/            ← Cleaned data, ready to use
├── notebooks/
│   ├── eda_analysis.ipynb    ← Step-by-step data exploration
│   └── RFM_Analysis.ipynb    ← Customer segmentation using RFM
├── reports/                  ← Output CSV and summary files
└── scripts/
    ├── extract.py            ← Data extraction
    └── clean.py              ← Data cleaning and preprocessing
```

---

## 2. Tools & Technology

| Tool | Purpose |
|---|---|
| Python | Primary programming language |
| Jupyter Notebook | Interactive analysis and visualization |
| pandas | Data manipulation and cleaning |
| Matplotlib / Seaborn | Data visualization |

---

## 3. How to Run This Project

Follow these steps. Beginner friendly.

**Step 1 — Download the project**
```bash
git clone https://github.com/biswajit-sasmal/online-retail-eda-pipeline.git
cd online-retail-eda-pipeline
```

**Step 2 — Install the required packages**
```bash
pip install pandas numpy matplotlib seaborn jupyter
```

**Step 3 — Clean the raw data first**
```bash
python scripts/extract.py
python scripts/clean.py
```

**Step 4 — Open the notebooks and explore**
```bash
jupyter notebook
```
Open `eda_analysis.ipynb` first, then `RFM_Analysis.ipynb`.

**Step 5 — Check the results**

All output files are saved inside the `reports/` folder.

---

## 4. Key Insights

Key findings from the analysis:

- 🥇 **Top 5 countries by revenue**: `top_5_country_based_on_sales.csv`
- 📦 **Top 5 products by quantity sold**: `top_5_product_based_on_quantity_sold.csv`
- 💰 **Top 5 products by total sales value**: `top_5_product_based_on_sales.csv`
- 📅 **Monthly sales for 2011** show seasonal patterns: `monthly_sales_2011.csv`
- 🧑‍🤝‍🧑 **Customer segments (RFM)**: loyal, at-risk, and new customers identified

---

## 5. Recommendations

Recommendations based on the analysis:

- 🎯 **Target marketing** to the top countries driving revenue
- 🔁 **Reward and retain loyal customers** identified by RFM
- 📦 **Prioritize inventory for top-selling products** to avoid stockouts
- 📅 **Plan inventory and promotions for seasonal peaks**
- ⚠️ **Re-engage at-risk customers** with tailored offers

---

## 6. Dataset Acknowledgement

The dataset used is the **Online Retail Dataset** from the [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/datasets/online+retail). It contains real transaction records from a UK-based non-registered online retail store for **2010–2011**.

---

## 7. Thank You

Thank you for taking the time to explore this project! 🙏

If this project is useful or you have suggestions, please open an issue or send feedback.

> *"Data is not just numbers — it tells a story. This project is one such story."*

---
<p align="center">Made with ❤️ and lots of ☕</p>