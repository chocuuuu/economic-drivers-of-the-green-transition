# Financing the Future: Economic Drivers of the Green Transition

![Python](https://img.shields.io/badge/python-3.8%2B-blue)
![Status](https://img.shields.io/badge/status-complete-green)

---

## Overview
This project analyzes the **Global Data on Sustainable Energy** to investigate the relationship between economic drivers—specifically **GDP growth** and **international financial aid**—and the transition to renewable energy.

Addressing **SDG 7 (Affordable and Clean Energy)** and **SDG 13 (Climate Action)**, the analysis answers three critical questions:
1.  **The Hidden Gap:** How does infrastructure access (electricity) compare to health-critical access (clean cooking)?
2.  **Aid Effectiveness:** Does international climate finance actually correlate with renewable capacity?
3.  **The Efficiency Paradox:** Has economic growth decoupled from energy intensity?

---

## Methodology Highlights
- **Decoupling Analysis:** Indexing Global GDP vs. Energy Intensity (2000–2019) to track efficiency gains.
- **Aid ROI Metrics:** Correlating cumulative financial flows with physical capacity added (Watts/capita) and checking for "Ghost Aid."
- **Stratified Analysis:** Breaking down renewable adoption by World Bank Income Quartiles (Low vs. High Income).
- **Trajectory Mapping:** Identifying "Top Mover" nations that achieved the highest growth in renewable share over the last two decades.

---

## Repository Contents

| File | Description |
|------|-------------|
| **`main.py`** | Main pipeline controller. Runs data loading, EDA, static visualization, and dashboard generation in sequence. |
| **`data_loader.py`** | Handles CSV ingestion, imputation of missing aid data, and feature engineering (Green Ratio, Income Groups). |
| **`eda.py`** | Performs statistical analysis for the paper, including correlations, intensity changes, and stratification by income. |
| **`visualizer.py`** | Generates the 9 static figures used in the final report, complete with granular data logging. |
| **`interactive_dashboard.py`** | Generates the HTML dashboard with interactive Plotly versions of all paper figures. |
| **`figures/`** | Directory containing all generated PNG plots and the HTML dashboard. |

---

## Instructions

<details>
<summary>1. Prerequisites</summary>

You need **Python 3.8+** and the following libraries:

```bash
pip install pandas numpy matplotlib seaborn plotly geopandas
```
</details>

<details> 
<summary>2. Running the Analysis</summary>

Place your dataset file global-data-on-sustainable-energy.csv in the data/ directory.

Run the main script:

```bash
python main.py
```

The script will execute in 4 Phases and log detailed statistics to the terminal for use in your report:

- **Phase 1**: Data Ingestion & Preprocessing.
- **Phase 2**: EDA (Decoupling stats, Aid correlations, Equity tables).
- **Phase 3**: Visualization Generation.
- **Phase 4**: Interactive Dashboard Assembly.

</details>

<details> <summary>3. Generated Outputs</summary>

After running the script, the figures/ directory will contain:

## Generated Outputs

After running the pipeline, the `figures/` directory will contain the following files:

### **1. Exploratory Data Analysis (EDA)**
* **`fig_eda_1_intensity_histogram.png`**: Distribution analysis of Energy Intensity (checking for skew).
* **`fig_eda_2_multi_boxplot.png`**: Outlier detection across key indicators (Access, Capacity, Intensity).
* **`fig_eda_3_missing_values.png`**: Summary of data gaps by column.

### **2. Main Report Figures**
* **`fig1_equity_gap.png`**: The "Hidden Gap" – Access to Electricity vs. Clean Cooking.
* **`fig2_aid_effectiveness.png`**: Scatter plot testing the correlation between Financial Aid and Renewable Capacity.
* **`fig3_efficiency_decoupling.png`**: Trends showing the separation of Economic Growth (GDP) from Energy Intensity.
* **`fig4_correlation_matrix.png`**: Heatmap of drivers (GDP, Aid, Renewable Share, etc.).
* **`fig5a_global_divergence.png`**: Global trends comparing GDP growth vs. CO₂ emissions.
* **`fig5b_strategic_leaders.png`**: Bar chart of the Top 20 nations by Renewable Capacity per capita.
* **`fig6_energy_mix.png`**: Stacked area chart showing the global share of Fossil Fuels vs. Renewables.
* **`fig7a_top_aid.png`**: Ranking of the top 10 recipients of international financial flows.
* **`fig7b_top_movers.png`**: Analysis of countries with the fastest growth in renewable energy share.
* **`fig8_income_disparity.png`**: Boxplot highlighting the "Green Divide" across income groups.
* **`fig9_forecast.png`**: Historical trajectories and future projections for top-performing nations.
* **`fig10_choropleth_map.png`**: Geospatial visualization of Global Renewable Capacity.

### **3. Interactive Output**
* **`interactive_dashboard.html`**: A standalone HTML file containing interactive Plotly versions of the figures above.

</details>

--- 

## Contributors
This project was authored by students from the College of Information and Computing Sciences at the University of Santo Tomas:
- Jade Vincent Alfonso – jadevincent.alfonso.cics@ust.edu.ph
- Ken Gerard Aguilar – kengerard.aguilar.cics@ust.edu.ph
- Racell Gabriel Sincioco – racellgabriel.sincioco.cics@ust.edu.ph