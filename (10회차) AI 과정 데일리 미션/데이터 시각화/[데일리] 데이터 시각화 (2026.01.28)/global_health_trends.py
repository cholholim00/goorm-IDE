import pandas as pd
import numpy as np
import os

# --- Step 0: Path Handling ---
# Find the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'global_health_trends.csv')

if not os.path.exists(file_path):
    print(f"❌ File not found: {file_path}")
    print("Please ensure 'global_health_trends.csv' is in the same folder as this script.")
else:
    # 1. Load the dataset (Everything must be inside this 'else' block)
    df = pd.read_csv(file_path)
    print(f"✅ Successfully loaded: {file_path}")

    # ---------------------------------------------------------
    # 1. Sorting (sort_values, sort_index)
    # ---------------------------------------------------------
    # Sort by Life Expectancy (Descending)
    df_sorted_val = df.sort_values(by='Life Expectancy', ascending=False)
    # Sort by Index (Row numbers)
    df_sorted_idx = df.sort_index()

    # ---------------------------------------------------------
    # 2. Top/Bottom Extraction (nlargest, nsmallest)
    # ---------------------------------------------------------
    # Extract Top 5 countries with highest Vaccination Coverage
    top_5_vaccination = df.nlargest(5, 'Vaccination Coverage (%)')
    # Extract Bottom 5 countries with lowest Infant Mortality Rate
    bottom_5_mortality = df.nsmallest(5, 'Infant Mortality Rate')

    # ---------------------------------------------------------
    # 3. Functional Combination (combine)
    # ---------------------------------------------------------
    df1 = df.head(10).copy()
    df2 = df.head(10).copy()
    df2['Disease Prevalence (%)'] = df2['Disease Prevalence (%)'] + 2.0
    # Combine picking the maximum value between Source A and Source B
    df_combined = df1.combine(df2, np.maximum)

    # ---------------------------------------------------------
    # 4. Index-based Merging (join)
    # ---------------------------------------------------------
    # Set 'Country' as index for joining
    df_health = df[['Country', 'Life Expectancy']].drop_duplicates('Country').set_index('Country')
    df_econ = df[['Country', 'GDP per Capita']].drop_duplicates('Country').set_index('Country')
    # Join horizontally based on the shared Index (Country)
    df_joined = df_health.join(df_econ, how='left')

    # ---------------------------------------------------------
    # 5. Key-based Merging (merge)
    # ---------------------------------------------------------
    # Splitting original df into two different metric sets
    df_metrics_a = df[['Country', 'Year', 'Vaccination Coverage (%)']]
    df_metrics_b = df[['Country', 'Year', 'Disease Prevalence (%)']]
    # Merge on common keys: 'Country' and 'Year'
    df_final_merge = pd.merge(df_metrics_a, df_metrics_b, on=['Country', 'Year'], how='inner')

    # ---------------------------------------------------------
    # Execution Results (Verification)
    # ---------------------------------------------------------
    print("\n--- [1] Top 5 Life Expectancy ---")
    print(df_sorted_val[['Country', 'Life Expectancy']].head())

    print("\n--- [2] Top 5 Vaccination Countries ---")
    print(top_5_vaccination[['Country', 'Vaccination Coverage (%)']])

    print("\n--- [3] Combine Result (Taking Maximum) ---")
    print(df_combined[['Country', 'Disease Prevalence (%)']].head())

    print("\n--- [4] Join Result (By Index) ---")
    print(df_joined.head())

    print("\n--- [5] Merge Result (By Key) ---")
    print(df_final_merge.head())