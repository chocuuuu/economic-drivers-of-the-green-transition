# filename: eda.py
import pandas as pd
import numpy as np

def perform_eda(df):
    """
    Prints robust statistical summaries for the ACM paper.
    Fixes NaNs, interprets intensity correctly, and adds grouping analysis.
    """
    print("\n" + "#"*60)
    print("   EXPLORATORY DATA ANALYSIS (EDA) - PAPER METRICS   ")
    print("#"*60)

    # 1. Dataset Integrity Check
    print(f"\n[1] Data Integrity")
    print(f"    - Total Records: {len(df)}")
    print(f"    - Countries: {df['Country'].nunique()}")
    print(f"    - Years: {df['Year'].min()} to {df['Year'].max()}")
    
    # 2. RQ1: The Decoupling Analysis (Growth vs Emissions)
    print(f"\n[2] RQ1: Economic Decoupling")
    if 'GDP_Capita' in df.columns and 'CO2_Total_kt' in df.columns:
        # Correlation
        corr_gdp_co2 = df[['GDP_Capita', 'CO2_Total_kt']].corr().iloc[0,1]
        print(f"    - Correlation (Wealth vs. Emissions): {corr_gdp_co2:.4f}")
        print("      -> Interpretation: Weak correlation implies broad variance (some decoupling).")

        # Energy Intensity Logic (Lower is Better)
        if 'Energy_Intensity' in df.columns:
            # Filter for valid years
            avg_2000 = df[df['Year'] == 2000]['Energy_Intensity'].mean()
            avg_2020 = df[df['Year'] == 2020]['Energy_Intensity'].mean()
            pct_change = ((avg_2020 - avg_2000) / avg_2000) * 100
            
            print(f"    - Global Avg Energy Intensity (2000): {avg_2000:.2f} MJ/$")
            print(f"    - Global Avg Energy Intensity (2020): {avg_2020:.2f} MJ/$")
            print(f"    - Change: {pct_change:+.2f}%")
            
            if pct_change > 0:
                print("      -> CRITICAL FINDING: Global efficiency has WORSENED (More energy needed per $).")
            else:
                print("      -> POSITIVE FINDING: Global efficiency has IMPROVED (Less energy needed per $).")

    # 3. RQ2: Aid Effectiveness (Cross-Sectional Analysis)
    print(f"\n[3] RQ2: Aid Effectiveness (ROI Analysis)")
    if 'Financial_Flows' in df.columns and 'Renewable_Capacity' in df.columns:
        # Group by Country to see if Total Aid -> Total Growth
        country_stats = df.groupby('Country').agg({
            'Financial_Flows': 'sum',
            'Renewable_Capacity': lambda x: x.max() - x.min()  # Growth proxy
        })
        
        # Filter for countries that actually received aid
        receivers = country_stats[country_stats['Financial_Flows'] > 1e6] # >$1M aid
        
        if not receivers.empty:
            corr_roi = receivers['Financial_Flows'].corr(receivers['Renewable_Capacity'])
            print(f"    - Total Aid Analyzed: ${country_stats['Financial_Flows'].sum()/1e9:.2f} Billion")
            print(f"    - ROI Correlation (Total Aid vs. Capacity Growth): {corr_roi:.4f}")
            print("      -> Interpretation: This is the 'True' effectiveness metric.")
        else:
            print("    - Insufficient data for Aid ROI analysis.")

    # 4. RQ3: The Equity Divide (Income Groups)
    print(f"\n[4] RQ3: Energy Equity by Income")
    if 'Income_Group' in df.columns and 'Renewable_Share' in df.columns:
        equity = df.groupby('Income_Group', observed=True)[['Access_Electricity', 'Renewable_Share', 'CO2_Total_kt']].mean()
        print(equity.to_string(float_format="{:.2f}".format))
        print("\n    -> Use this table to discuss the 'Green Divide' in your Discussion section.")

    # 5. Top Performers (Cleaned)
    print(f"\n[5] Top Performers (2020 - Cleaned)")
    df_2020 = df[df['Year'] == 2020].copy()
    
    # Drop NaNs before ranking to avoid 'Afghanistan NaN' issue
    top_share = df_2020.dropna(subset=['Renewable_Share']).nlargest(5, 'Renewable_Share')
    print("    - Top 5 by Renewable Share (%):")
    print(top_share[['Country', 'Renewable_Share']].to_string(index=False))

    print("\n" + "#"*60 + "\n")