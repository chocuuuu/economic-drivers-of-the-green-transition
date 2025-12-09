# filename: eda.py
import pandas as pd
import numpy as np

# Global setting for analysis year
LAST_VALID_YEAR = 2019

def perform_eda(df):
    """
    Prints stats using 2019 as the final year to avoid 2020 data gaps.
    """
    print("\n" + "="*50)
    print(f"   PHASE 2: EXPLORATORY DATA ANALYSIS (EDA) [2000-{LAST_VALID_YEAR}]   ")
    print("="*50)

    # 1. Integrity
    print(f"\n[1] Data Integrity")
    print(f"    - Unique Countries: {df['Country'].nunique()}")
    print(f"    - Analysis Window: 2000 to {LAST_VALID_YEAR}")

    # 2. RQ1: Decoupling
    print(f"\n[2] RQ1: Economic Decoupling")
    # Filter for valid years only
    df_valid = df[df['Year'] <= LAST_VALID_YEAR]
    
    if 'GDP_Capita' in df_valid.columns and 'CO2_Total_kt' in df_valid.columns:
        corr_gdp_co2 = df_valid[['GDP_Capita', 'CO2_Total_kt']].corr().iloc[0,1]
        print(f"    - Correlation (Wealth vs. Emissions): {corr_gdp_co2:.4f}")

        if 'Energy_Intensity' in df_valid.columns:
            avg_2000 = df[df['Year'] == 2000]['Energy_Intensity'].mean()
            avg_last = df[df['Year'] == LAST_VALID_YEAR]['Energy_Intensity'].mean()
            
            # Avoid division by zero
            if avg_2000 and avg_2000 > 0:
                pct_change = ((avg_last - avg_2000) / avg_2000) * 100
                print(f"    - Energy Intensity (2000): {avg_2000:.2f} MJ/$")
                print(f"    - Energy Intensity ({LAST_VALID_YEAR}): {avg_last:.2f} MJ/$")
                print(f"    - Change: {pct_change:+.2f}%")
                
                if pct_change > 0:
                    print("      (!) ALERT: Efficiency WORSENED (or check data quality).")
                else:
                    print("      (OK) Insight: Efficiency IMPROVED.")

    # 3. RQ2: Aid Effectiveness
    print(f"\n[3] RQ2: Aid ROI Analysis")
    if 'Financial_Flows' in df.columns:
        total_aid = df['Financial_Flows'].sum()
        print(f"    - Total Aid Recorded (All Years): ${total_aid/1e9:.2f} Billion")
        
        receivers = df_valid[df_valid['Financial_Flows'] > 0]
        if not receivers.empty and 'Renewable_Capacity' in receivers.columns:
            corr_aid = receivers['Financial_Flows'].corr(receivers['Renewable_Capacity'])
            print(f"    - Correlation (Aid > 0 vs Capacity): {corr_aid:.4f}")

    # 4. RQ3: Equity
    print(f"\n[4] RQ3: The Green Divide")
    if 'Income_Group' in df.columns:
        print(f"    - Avg Renewable Share ({LAST_VALID_YEAR}):")
        print(df[df['Year'] == LAST_VALID_YEAR].groupby('Income_Group', observed=True)['Renewable_Share'].mean().to_string())

    print("\n" + "="*50)